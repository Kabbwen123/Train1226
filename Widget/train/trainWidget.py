import json
import platform
from datetime import datetime
from pathlib import Path
from typing import Optional
import subprocess, shutil
import yaml
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget, QMessageBox, QInputDialog,
)

from Application.ProjectDataClass import Project, Model
from Infrastructure.sqlDB import SqlDB
from Interface.UI.train.trainUI import Ui_Form
from Interface.Widget.assess.assessDialog import AssessDialog
from Interface.Widget.pjtInfoWidget import PjtInfoWidget
from Interface.Widget.train.modelCardWidget import ModelCardWidget
from Interface.Widget.train.okNgTrainTestWidget import OkNgTrainTestWidget
from Interface.qtBridge import QtBridge

CONFIG_PATH = "Config\config_setting.yaml"


class TrainWidget(QWidget, Ui_Form):

    def __init__(self,
                 sql_db: Optional[SqlDB] = None,
                 bridge: Optional[QtBridge] = None,
                 project: Optional[Project] = None,
                 parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.sql_db = sql_db
        self.bridge = bridge
        self.project = project
        self._selected_model: Model | None = None
        self._model_records: dict[int, dict] = {}
        self._training_model_id: int | None = None
        self._training_progress: float = 0.0

        self._init_faiss_widget()
        self._init_model_area()
        self._reload_model_cards()

        # 数据集
        self.dataset_widget = OkNgTrainTestWidget()
        self.gridLayout_4.addWidget(self.dataset_widget)
        self._update_dataset_rows()

        self.set_default()
        self.deviceCbx.addItems(get_device_info())

        self.faissCmb.currentTextChanged.connect(self._update_faiss_widget)
        self._update_faiss_widget(self.faissCmb.currentText())

        # 按钮事件
        self.btnCreateModel.clicked.connect(self.create_model)
        self.saveCfgBtn.clicked.connect(self.save_config)
        self.btnPlay.clicked.connect(self._on_play_clicked)
        self.btnAssess.clicked.connect(self._on_assess_clicked)
        self._update_action_buttons()

        self.bridge.train_result_emitted.connect(self._on_train_result)

    @Slot()
    def create_model(self):
        if not self.project or not self.sql_db:
            QMessageBox.warning(self, "新建模型", "请先选择项目")
            return
        data = {
            "project_id": self.project.id,
            "model_name": f"Train {datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}",
            "create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        try:
            new_id = self.sql_db.insert("model", data)
            self._selected_model = Model(
                new_id,
                data["project_id"],
                data["model_name"],
                None,
                None,
                data["create_time"],
                None,
            )
            self._reload_model_cards()
        except Exception as e:
            QMessageBox.critical(
                self,
                "新建模型",
                f"新建模型失败: {e}",
            )

    def set_project(self, project: Optional[Project]):
        self.project = project
        self._selected_model = None

        v_layout = self.pjtInfoFrame.layout()
        if not v_layout.count() and project:
            v_layout.addWidget(PjtInfoWidget(project))

        self._update_dataset_rows()
        self._reload_model_cards()
        self._update_action_buttons()

    @Slot()
    def _on_play_clicked(self):
        if self._selected_model is None:
            QMessageBox.warning(self, "开始训练", "请先选择或新建模型")
            return
        config = self._selected_model.config
        dataset = self._selected_model.dataset
        if config is None or dataset is None:
            QMessageBox.warning(self, "开始训练", "获取有效配置或数据集失败，请重新配置并保存")
            return

        path_list = []
        project_dir = Path("Project") / self.project.name
        dataset_dir = project_dir / "Dataset"
        print(dataset)
        for key, val in dataset.get("state", {}).get("OK", {}).items():
            if val.get("train"):
                path_list.append(str(dataset_dir / "OK" / key))
        self._set_training_state(True, self._selected_model.id)
        self.bridge.start_train(self._selected_model.id, config, path_list, str(project_dir / "Models"))

    @Slot(int, float, str)
    def _on_train_result(self, model_id: int, pgs: float, path: str):
        print("_on_train_result", model_id, pgs, path)
        self._training_progress = pgs
        self._update_training_progress(model_id, pgs)
        if path:
            self._training_progress = 100.0
            self._update_training_progress(model_id, 100.0, visible=False)
            if self.sql_db:
                self.sql_db.update("model", {"path": path}, '"id" = ?', [model_id])
                self._update_cached_model_record(model_id, path=path)
            self._set_training_state(False, None)
            self._update_action_buttons()

    @Slot()
    def _on_assess_clicked(self):
        if self._selected_model is None:
            QMessageBox.warning(self, "模型评估", "请先选择或新建模型")
            return
        if not self._selected_model_has_path():
            QMessageBox.warning(self, "模型评估", "模型尚未训练，请先完成训练")
            return
        if self._selected_model_has_assess_results():
            dialog = AssessDialog(sql_db=self.sql_db, bridge=self.bridge, model=self._selected_model, parent=self)
            dialog.exec()
            self._update_action_buttons()
            return

        if self._selected_model.dataset is None:
            QMessageBox.warning(self, "模型评估", "获取有效数据集失败，请重新配置并保存")
            return
        dialog = AssessDialog(sql_db=self.sql_db, bridge=self.bridge, model=self._selected_model, parent=self)

        path_list = []
        project_dir = Path("Project") / self.project.name
        dataset_dir = project_dir / "Dataset"
        for key, val in self._selected_model.dataset.get("state", {}).items():
            for keyy, vals in val.items():
                if vals.get("test"):
                    path_list.append((key, str(dataset_dir / key / keyy)))
        self.bridge.start_assess(self._selected_model.id, path_list, self._selected_model.path)

        dialog.exec()
        self._update_action_buttons()

    def _update_action_buttons(self):
        has_path = self._selected_model_has_path()
        has_assess_data = self._selected_model_has_assess_results()
        is_training = self._training_model_id is not None
        self.btnAssess.setEnabled(has_path)
        self.btnPlay.setEnabled(not has_path and not is_training)
        self._set_main_panel_enabled(not has_path)
        if has_path and has_assess_data:
            self.btnAssess.setText("评估数据")
        else:
            self.btnAssess.setText("开始评估")

    def _init_model_area(self):
        layout = QVBoxLayout(self.scrollAreaWidgetContents)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.model_list_layout = layout
        self._model_cards = []

    def _clear_model_cards(self):
        while self.model_list_layout.count():
            item = self.model_list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def _reload_model_cards(self):
        self._clear_model_cards()
        self._model_cards = []
        self._model_records = {}

        if not self.project or not self.sql_db:
            return

        records = [
            dict(r) for r in self.sql_db.fetch_all(
                "model",
                columns='*',
                where_clause='"project_id" = ? ORDER BY "create_time" DESC',
                params=[self.project.id],
            )
        ]
        self._model_records = {int(record["id"]): record for record in records}
        for record in records:
            model_id = int(record["id"])
            card = ModelCardWidget(self.scrollAreaWidgetContents)
            card.set_model(
                model_id=model_id,
                name=record["model_name"],
                created_at=record["create_time"]
            )
            card.clicked.connect(self._on_card_clicked)
            card.editRequested.connect(self._on_card_edit)
            card.deleteRequested.connect(self._on_card_delete)
            if self._selected_model and model_id == self._selected_model.id:
                card.set_selected(True)
            self.model_list_layout.addWidget(card)
            self._model_cards.append(card)
        self.model_list_layout.addStretch()
        self._restore_training_progress()
        self._update_action_buttons()

        if not records:
            self._selected_model = None
            self.set_default()
            self._update_action_buttons()
            return

        if records:
            ids = [r["id"] for r in records]
            selected_id = self._selected_model.id if self._selected_model else None
            if selected_id not in ids:
                self._on_card_clicked(ids[0])
            else:
                self._selected_model = Model(**self._model_records[selected_id])
                self._highlight_selected_card()
                self._load_model_settings(self._selected_model)
                self._update_action_buttons()

    def _highlight_selected_card(self):
        for card in self._model_cards:
            selected_id = self._selected_model.id if self._selected_model else None
            card.set_selected(card.model_id() == selected_id)

    def _on_card_clicked(self, model_id: int):
        record = self._get_model_record(model_id)
        self._selected_model = Model(**record) if record else None
        self._highlight_selected_card()
        self._load_model_settings(self._selected_model)
        self._update_action_buttons()

    def _on_card_edit(self, model_id: int):
        if not self.sql_db:
            return
        record = self._get_model_record(model_id)
        current_name = record["model_name"] if record else ""
        new_name, ok = QInputDialog.getText(self, "修改模型名称", "模型名称", text=current_name or "")
        if ok and new_name:
            self.sql_db.update("model", {"model_name": new_name}, '"id" = ?', [model_id])
            self._update_cached_model_record(model_id, model_name=new_name)
            if self._selected_model and self._selected_model.id == model_id:
                self._refresh_selected_model(model_id)
            self._reload_model_cards()
            self._update_action_buttons()

    def _on_card_delete(self, model_id: int):
        if not self.sql_db:
            return
        reply = QMessageBox.question(
            self,
            "删除模型",
            "确定要删除该模型吗？该操作不可撤销。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.sql_db.delete("model", '"id" = ?', [model_id])
            if self._selected_model and self._selected_model.id == model_id:
                self._selected_model = None
            if self._training_model_id == model_id:
                self._set_training_state(False, None)
            self._reload_model_cards()

    def _load_model_settings(self, model: Model | None):
        if not self.sql_db or model is None:
            self.set_default()
            self._update_action_buttons()
            return

        record = self._get_model_record(model.id)
        if not record:
            self.set_default()
            self._update_action_buttons()
            return

        try:
            cfg_data = json.loads(record["config"])
            self._apply_config(cfg_data)
        except Exception:
            self.set_default()

        dataset_raw = record.get("dataset") if isinstance(record, dict) else record["dataset"]
        try:
            dataset_data = json.loads(dataset_raw) if dataset_raw else None
        except Exception:
            dataset_data = None
        self._apply_dataset_state(dataset_data)
        self._update_action_buttons()

    def _get_model_record(self, model_id: int | None) -> dict | None:
        if model_id is None:
            return None
        record = self._model_records.get(model_id)
        if record is not None:
            return record
        if not self.sql_db:
            return None
        row = self.sql_db.fetch_one("model", where_clause='"id" = ?', params=[model_id])
        if row:
            record = dict(row)
            self._model_records[model_id] = record
            return record
        return None

    def _update_cached_model_record(self, model_id: int | None, **kwargs):
        if model_id is None:
            return
        if model_id in self._model_records:
            self._model_records[model_id].update(kwargs)
        if self._selected_model and self._selected_model.id == model_id:
            for key, value in kwargs.items():
                if hasattr(self._selected_model, key):
                    setattr(self._selected_model, key, value)

    def _refresh_selected_model(self, model_id: int | None):
        if model_id is None:
            return
        record = self._get_model_record(model_id)
        if record:
            self._selected_model = Model(**record)

    def _set_training_state(self, active: bool, model_id: int | None):
        if active:
            self.btnPlay.setEnabled(False)
            self._training_model_id = model_id
            self._training_progress = 0.0
            self._update_training_progress(model_id, 0.0, visible=True)
        else:
            self._update_training_progress(self._training_model_id, self._training_progress, visible=False)
            self._training_model_id = None
            self._training_progress = 0.0
            self._update_action_buttons()

    def _update_training_progress(self, model_id: int | None, pgs: float, visible: bool | None = None):
        if model_id is None:
            return
        for card in self._model_cards:
            if card.model_id() == model_id:
                card.set_progress(pgs)
                if visible is not None:
                    card.set_progress_visible(visible)
            else:
                if visible is not None and visible:
                    card.set_progress_visible(False)

    def _restore_training_progress(self):
        if self._training_model_id is None:
            return
        self._update_training_progress(self._training_model_id, self._training_progress, visible=True)

    def _selected_model_has_path(self) -> bool:
        if self._selected_model is None:
            return False
        if self._selected_model.path:
            return True
        record = self._get_model_record(self._selected_model.id)
        if record and record.get("path"):
            self._selected_model.path = record.get("path")
            return True
        return False

    def _selected_model_has_assess_results(self) -> bool:
        if self._selected_model is None or not self.sql_db:
            return False
        row = self.sql_db.fetch_one(
            "assessResult",
            columns='COUNT(*) AS "cnt"',
            where_clause='"model_id" = ?',
            params=[self._selected_model.id],
        )
        if not row:
            return False
        return int(row["cnt"]) > 0

    def _set_main_panel_enabled(self, enabled: bool):
        self._set_layout_enabled(self.verticalLayout_main_2, enabled)

    def _set_layout_enabled(self, layout, enabled: bool):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.setEnabled(enabled)
                continue
            child_layout = item.layout()
            if child_layout is not None:
                self._set_layout_enabled(child_layout, enabled)

    def _init_faiss_widget(self):
        self.faiss_layout = self.faissWidget.layout()
        self.faiss_layout.setContentsMargins(0, 0, 0, 0)

        self.ivf_nlist_label = QLabel("ivf_nlist", self.faissWidget)
        self.ivf_nlist_spin = QSpinBox(self.faissWidget)
        self.ivf_nlist_spin.setMinimum(1)
        self.ivf_nlist_spin.setMaximum(999999)
        self.ivf_nlist_spin.setValue(2048)

        self.ivf_nprobe_label = QLabel("ivf_nprobe", self.faissWidget)
        self.ivf_nprobe_spin = QSpinBox(self.faissWidget)
        self.ivf_nprobe_spin.setMinimum(1)
        self.ivf_nprobe_spin.setMaximum(9999)
        self.ivf_nprobe_spin.setValue(20)

        self.pq_m_label = QLabel("pq_m", self.faissWidget)
        self.pq_m_spin = QSpinBox(self.faissWidget)
        self.pq_m_spin.setMinimum(1)
        self.pq_m_spin.setMaximum(512)
        self.pq_m_spin.setValue(32)

        self.pq_nbits_label = QLabel("pq_nbits", self.faissWidget)
        self.pq_nbits_spin = QSpinBox(self.faissWidget)
        self.pq_nbits_spin.setMinimum(1)
        self.pq_nbits_spin.setMaximum(32)
        self.pq_nbits_spin.setValue(8)

        self.hnsw_m_label = QLabel("hnsw_m", self.faissWidget)
        self.hnsw_m_spin = QSpinBox(self.faissWidget)
        self.hnsw_m_spin.setMinimum(1)
        self.hnsw_m_spin.setMaximum(512)
        self.hnsw_m_spin.setValue(32)

        self.hnsw_ef_construction_label = QLabel("hnsw_ef_construction", self.faissWidget)
        self.hnsw_ef_construction_spin = QSpinBox(self.faissWidget)
        self.hnsw_ef_construction_spin.setMinimum(1)
        self.hnsw_ef_construction_spin.setMaximum(5000)
        self.hnsw_ef_construction_spin.setValue(200)

        self.hnsw_ef_search_label = QLabel("hnsw_ef_search", self.faissWidget)
        self.hnsw_ef_search_spin = QSpinBox(self.faissWidget)
        self.hnsw_ef_search_spin.setMinimum(1)
        self.hnsw_ef_search_spin.setMaximum(5000)
        self.hnsw_ef_search_spin.setValue(128)

        self.faiss_layout.addRow(self.ivf_nlist_label, self.ivf_nlist_spin)
        self.faiss_layout.addRow(self.ivf_nprobe_label, self.ivf_nprobe_spin)
        self.faiss_layout.addRow(self.pq_m_label, self.pq_m_spin)
        self.faiss_layout.addRow(self.pq_nbits_label, self.pq_nbits_spin)
        self.faiss_layout.addRow(self.hnsw_m_label, self.hnsw_m_spin)
        self.faiss_layout.addRow(self.hnsw_ef_construction_label, self.hnsw_ef_construction_spin)
        self.faiss_layout.addRow(self.hnsw_ef_search_label, self.hnsw_ef_search_spin)

    def _hide_all_faiss_controls(self):
        self.ivf_nlist_label.hide()
        self.ivf_nlist_spin.hide()
        self.ivf_nprobe_label.hide()
        self.ivf_nprobe_spin.hide()
        self.pq_m_label.hide()
        self.pq_m_spin.hide()
        self.pq_nbits_label.hide()
        self.pq_nbits_spin.hide()
        self.hnsw_m_label.hide()
        self.hnsw_m_spin.hide()
        self.hnsw_ef_construction_label.hide()
        self.hnsw_ef_construction_spin.hide()
        self.hnsw_ef_search_label.hide()
        self.hnsw_ef_search_spin.hide()

    def _update_faiss_widget(self, text: str):
        self._hide_all_faiss_controls()

        if text == "IVFFlat":
            self.ivf_nlist_label.show()
            self.ivf_nlist_spin.show()
            self.ivf_nprobe_label.show()
            self.ivf_nprobe_spin.show()
        elif text == "IVFPQ":
            self.pq_m_label.show()
            self.pq_m_spin.show()
            self.pq_nbits_label.show()
            self.pq_nbits_spin.show()
        elif text == "HNSW":
            self.hnsw_m_label.show()
            self.hnsw_m_spin.show()
            self.hnsw_ef_construction_label.show()
            self.hnsw_ef_construction_spin.show()
            self.hnsw_ef_search_label.show()
            self.hnsw_ef_search_spin.show()

    def _update_dataset_rows(self):
        ok, ng = self.get_dataset()
        self.dataset_widget.set_rows(ok=ok, ng=ng)

    def get_dataset(self):
        ok: list[tuple[str, int]] = []
        ng: list[tuple[str, int]] = []
        if not self.sql_db or not self.project:
            return ok, ng
        records = self.sql_db.fetch_all(
            "image",
            columns='\"tag\",\"subtag\", COUNT(*) AS "cnt"',
            where_clause='\"project_id\" = ? GROUP BY \"tag\",\"subtag\"',
            params=[self.project.id],
        )
        for r in records:
            tag = (r["tag"] or "").strip()
            subtag = (r["subtag"] or "")
            count = int(r["cnt"])
            if tag == "OK":
                ok.append((subtag, count))
            elif tag == "NG":
                ng.append((subtag, count))
        return ok, ng

    def set_default(self):
        cfg = load_yaml(CONFIG_PATH)
        self._apply_config(cfg)

    @Slot()
    def save_config(self):
        if not self.project:
            QMessageBox.warning(self, "保存配置", "请先选择项目")
            return
        if not self.sql_db:
            QMessageBox.warning(self, "保存配置", "数据库未初始化")
            return
        if self._selected_model is None:
            QMessageBox.warning(self, "保存配置", "请先选择或新建模型")
            return

        cfg = self._collect_config_from_form()
        dataset_state = self._collect_dataset_state()

        cfg_json = json.dumps(cfg, ensure_ascii=False)
        dataset_json = json.dumps(dataset_state, ensure_ascii=False)

        try:
            self.sql_db.update(
                "model",
                {
                    "config": cfg_json,
                    "dataset": dataset_json,
                },
                '"id" = ?',
                [self._selected_model.id],
            )
            self._update_cached_model_record(
                self._selected_model.id,
                config=cfg_json,
                dataset=dataset_json,
            )
            self._refresh_selected_model(self._selected_model.id)
            self._show_floating_message("保存配置", "配置保存成功")
        except Exception as e:
            QMessageBox.critical(self, "保存配置", f"保存失败: {e}")

    def _collect_config_from_form(self) -> dict:
        cfg = dict()

        # model
        model = dict()
        model["backbone_name"] = self.backbone_nameCmb.currentText()
        model["input_size"] = [self.input_sizeHSpb.value(), self.input_sizeWSpb.value()]
        model["patch_size"] = self.patch_sizeSpb.value()
        embedding_layers = []
        if self.embedding1Cbx.isChecked():
            embedding_layers.append("1")
        if self.embedding2Cbx.isChecked():
            embedding_layers.append("2")
        if self.embedding3Cbx.isChecked():
            embedding_layers.append("3")
        if self.embedding4Cbx.isChecked():
            embedding_layers.append("4")
        model["embedding_layers"] = "_".join(embedding_layers)
        cfg["model"] = model

        # train
        train = dict()
        train["batch_size"] = int(self.batch_sizeCmb.currentText())
        train["seed"] = int(self.seedSpb.value())
        train["max_train_features"] = int(self.max_train_featuresSpb.value())
        train["n_neighbors"] = int(self.neighborsCmb.currentText())
        # TODO 传参 gpu_device_id
        cfg["train"] = train

        # coreset
        cfg["coreset"] = {"method": self.coresetCmb.currentText()}

        # faiss
        faiss = dict()
        faiss_type = self.faissCmb.currentText()
        faiss["index_type"] = faiss_type
        if faiss_type == "IVFFlat":
            faiss["ivf_nlist"] = self.ivf_nlist_spin.value()
            faiss["ivf_nprobe"] = self.ivf_nprobe_spin.value()
        elif faiss_type == "IVFPQ":
            faiss["pq_m"] = self.pq_m_spin.value()
            faiss["pq_nbits"] = self.pq_nbits_spin.value()
        elif faiss_type == "HNSW":
            faiss["hnsw_m"] = self.hnsw_m_spin.value()
            faiss["hnsw_ef_construction"] = self.hnsw_ef_construction_spin.value()
            faiss["hnsw_ef_search"] = self.hnsw_ef_search_spin.value()
        cfg["faiss"] = faiss

        return cfg

    def _apply_config(self, cfg: Optional[dict]):
        merged_cfg = load_yaml(CONFIG_PATH)
        merged_cfg = _merge_dicts(merged_cfg, cfg or {})

        model_cfg = merged_cfg.get("model", {})
        self.backbone_nameCmb.setCurrentText(model_cfg.get("backbone_name", "resnet34"))
        input_size = model_cfg.get("input_size", [256, 640])
        if isinstance(input_size, (list, tuple)) and len(input_size) == 2:
            self.input_sizeHSpb.setValue(int(input_size[0]))
            self.input_sizeWSpb.setValue(int(input_size[1]))
        self.patch_sizeSpb.setValue(int(model_cfg.get("patch_size", 3)))

        embedding_layers = model_cfg.get("embedding_layers", "2_3")
        if isinstance(embedding_layers, (list, tuple)):
            embedding_layers_set = {str(v) for v in embedding_layers}
        else:
            embedding_layers_set = set(str(embedding_layers).split("_")) if embedding_layers else set()
        self.embedding1Cbx.setChecked("1" in embedding_layers_set)
        self.embedding2Cbx.setChecked("2" in embedding_layers_set)
        self.embedding3Cbx.setChecked("3" in embedding_layers_set)
        self.embedding4Cbx.setChecked("4" in embedding_layers_set)

        train_cfg = merged_cfg.get("train", {})
        self.batch_sizeCmb.setCurrentText(str(train_cfg.get("batch_size", 16)))
        self.seedSpb.setValue(int(train_cfg.get("seed", 42)))
        self.max_train_featuresSpb.setValue(int(train_cfg.get("max_train_features", 200000)))
        self.neighborsCmb.setCurrentText(str(train_cfg.get("n_neighbors", 5)))

        coreset_cfg = merged_cfg.get("coreset", {})
        self.coresetCmb.setCurrentText(coreset_cfg.get("method", "random"))

        faiss_cfg = merged_cfg.get("faiss", {})
        faiss_type = faiss_cfg.get("index_type", "Flat")
        if self.faissCmb.findText(faiss_type) == -1:
            faiss_type = "Flat"
        self.faissCmb.setCurrentText(faiss_type)
        self._update_faiss_widget(faiss_type)
        if faiss_type == "IVFFlat":
            self.ivf_nlist_spin.setValue(int(faiss_cfg.get("ivf_nlist", 2048)))
            self.ivf_nprobe_spin.setValue(int(faiss_cfg.get("ivf_nprobe", 20)))
        elif faiss_type == "IVFPQ":
            self.pq_m_spin.setValue(int(faiss_cfg.get("pq_m", 32)))
            self.pq_nbits_spin.setValue(int(faiss_cfg.get("pq_nbits", 8)))
        elif faiss_type == "HNSW":
            self.hnsw_m_spin.setValue(int(faiss_cfg.get("hnsw_m", 32)))
            self.hnsw_ef_construction_spin.setValue(int(faiss_cfg.get("hnsw_ef_construction", 200)))
            self.hnsw_ef_search_spin.setValue(int(faiss_cfg.get("hnsw_ef_search", 128)))

    def _apply_dataset_state(self, dataset_data: Optional[dict]):
        ok, ng = self.get_dataset()
        self.dataset_widget.set_rows(ok=ok, ng=ng)

        if not dataset_data:
            return

        saved_snapshot = dataset_data.get("snapshot")
        saved_state = dataset_data.get("state")
        current_snapshot = self._serialize_dataset_snapshot(ok, ng)

        if saved_snapshot is not None and not self._snapshot_matches(saved_snapshot, current_snapshot):
            QMessageBox.warning(self, "数据集变更", "当前数据集存在变更，请重新设置")
            return

        if saved_state:
            self.dataset_widget.set_state(saved_state)

    def _collect_dataset_state(self) -> dict:
        ok, ng = self.get_dataset()
        return {
            "snapshot": self._serialize_dataset_snapshot(ok, ng),
            "state": self.dataset_widget.to_state(),
        }

    @staticmethod
    def _serialize_dataset_snapshot(ok: list[tuple[str, int]], ng: list[tuple[str, int]]) -> dict:
        return {
            "OK": [{"name": name, "count": int(count)} for name, count in ok],
            "NG": [{"name": name, "count": int(count)} for name, count in ng],
        }

    @staticmethod
    def _snapshot_matches(saved_snapshot: dict, current_snapshot: dict) -> bool:
        def normalize(snapshot: dict, key: str):
            items = snapshot.get(key, []) if isinstance(snapshot, dict) else []
            normalized: list[tuple[str, int]] = []
            for item in items:
                if isinstance(item, dict):
                    name = str(item.get("name", ""))
                    count = int(item.get("count", 0))
                elif isinstance(item, (list, tuple)) and len(item) >= 2:
                    name = str(item[0])
                    count = int(item[1])
                else:
                    name = str(item)
                    count = 0
                normalized.append((name, count))
            return sorted(normalized)

        return (
                normalize(saved_snapshot, "OK") == normalize(current_snapshot, "OK")
                and normalize(saved_snapshot, "NG") == normalize(current_snapshot, "NG")
        )

    def _show_floating_message(self, title: str, text: str):
        QMessageBox.information(self, title, text)


def _merge_dicts(base: dict, override: dict) -> dict:
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = _merge_dicts(base.get(k, {}), v)
        else:
            base[k] = v
    return base


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)  # None / dict / list
    return data or {}


def get_device_info():
    # cpu
    info = [f"cpu:{platform.processor() or platform.uname().processor}"]
    # nvidia_info
    if not shutil.which("nvidia-smi"):  # 非 NVIDIA 平台
        return info
    cmd = [
        "nvidia-smi",
        "--query-gpu=index,name,memory.used,memory.total,temperature.gpu,utilization.gpu",
        "--format=csv,noheader,nounits"
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    for line in out.splitlines():
        idx, name, mem_used, mem_total, temp, util = line.split(", ")
        info.append(f"{name.strip()}(gpu:{int(idx)})")
    return info
