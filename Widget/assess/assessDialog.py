import os
import sys
from dataclasses import dataclass
from typing import Optional, List

from PySide6.QtWidgets import QHBoxLayout, QApplication, QVBoxLayout, QDialog

from Application.ProjectDataClass import Model, AssessResult, ImgDetailData
from Infrastructure.sqlDB import SqlDB
from Interface.UI.assess.assessmentUI import Ui_Dialog
from Interface.Widget.assess.histogramThresholdWidget import HistogramThresholdWidget
from Interface.Widget.assess.imgWidget import ImgWidget
from Interface.Widget.assess.pieChartWidget import PieChartWidget
from Interface.Widget.assess.matrixWidget import MatrixWidget
from Interface.qtBridge import QtBridge


@dataclass
class MATRIX:
    OKGOOD = 1
    OKBAD = 2
    NGGOOD = 3
    NGBAD = 4

    OKSUM = 5
    NGSUM = 6
    PREOKSUM = 7
    PRENGUM = 8


class AssessDialog(QDialog, Ui_Dialog):

    def __init__(self,
                 sql_db: Optional[SqlDB] = None,
                 bridge: Optional[QtBridge] = None,
                 model: Optional[Model] = None,
                 parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.sql_db = sql_db
        self.bridge = bridge
        self.model = model

        # ————————————————————————————图表所需数据——————————————————————
        self.all_data = []
        self.threshold = 100

        self.ok_true = []  # ok为预测为正，true即真实为正
        self.ok_false = []
        self.ng_false = []
        self.ng_true = []

        self.ok_list = []
        self.ng_list = []
        # ————————————————————————布局————————————————————————————————
        # 饼图
        self.pieLayout = QHBoxLayout(self.pieOkNgHost)
        self.pieLayout.setContentsMargins(0, 0, 0, 0)
        self.pieLayout.setSpacing(6)
        self._pie_chart()
        # 混淆矩阵
        self._init_matrix()
        # 评分直方图
        self._init_score_histogram()
        # 图像画廊
        self._init_image_gallery()
        self._show_converted_images = False

        self._init_data()  # 初始化数据

        # 接收评估结果
        self.bridge.assess_result_emitted.connect(self._signal_update)

    def _init_data(self):
        self.all_data = []
        if not self.sql_db or not self.model or self.model.id is None:
            return

        rows = self.sql_db.fetch_all(
            "assessResult",
            columns="*",
            where_clause='"model_id" = ?',
            params=[self.model.id],
        )
        for row in rows:
            assess_rst = AssessResult(*row)
            self.all_data.append(assess_rst)
            # 直方图列表数据初始化
            if assess_rst.tag == "OK":
                self.ok_list.append(assess_rst.score)
            elif assess_rst.tag == "NG":
                self.ng_list.append(assess_rst.score)
        # self._update_data()

    def _signal_update(self, model_id, tag, label, score, path, path_cvt, defect_count, detect_time):
        # 接收评估返回信息
        assess_data = {
            "model_id": model_id,
            "tag": tag,
            "label": label,
            "score": score,
            "img_path": path,
            "img_path_cvt": path_cvt,
            "defect_count": defect_count,
            "detect_time": detect_time,
        }
        if self.sql_db:
            assess_id = self.sql_db.insert("assessResult", assess_data)
        else:
            assess_id = None
        assess_result = AssessResult(
            assess_id,
            model_id,
            tag,
            label,
            score,
            path,
            path_cvt,
            defect_count,
            detect_time,
        )
        self.all_data.append(assess_result)
        # 图像画廊
        if self.imgWidget:
            img_path = path
            if img_path:
                self.imgWidget.add_image(img_path, assess_result)
        # 直方图
        if tag == "OK":
            self.ok_list.append(score)
        elif tag == "NG":
            self.ng_list.append(score)
        # 综合指标、混淆矩阵
        self._update_data()

    def _update_data(self):
        """all_data更新后的数据处理"""
        if not self.all_data:
            return
        self.ok_true = []
        self.ok_false = []
        self.ng_false = []
        self.ng_true = []

        cost_time = 0
        for assess_rst in self.all_data:
            cost_time += assess_rst.detect_time
            if assess_rst.tag == "OK":
                # TODO > 还是 >= ?
                if assess_rst.score > self.threshold:
                    self.ok_false.append(assess_rst)
                else:
                    self.ok_true.append(assess_rst)
            elif assess_rst.tag == "NG":
                if assess_rst.score > self.threshold:
                    self.ng_false.append(assess_rst)
                else:
                    self.ng_true.append(assess_rst)
        ok_ok = len(self.ok_true)
        ok_ng = len(self.ok_false)
        ng_ok = len(self.ng_true)
        ng_ng = len(self.ng_false)
        # 饼图数据(综合指标)
        self._update_pie_chart(len(self.all_data), cost_time, ok_ok, ok_ng, ng_ok, ng_ng)
        # 混淆矩阵
        self.matrixWidget.update_date(ok_ok, ok_ng, ng_ok, ng_ng)

    def _pie_chart(self):
        data = {
            "OK": 1,
            "NG": 1,
        }
        self.precisionPie = PieChartWidget(self.pieOkNgHost)
        self.precisionPie.set_title("精确率：--%")
        self.precisionPie.set_color_map({
            "OK": "#4CAF50",  # 绿色
            "NG": "#9E9E9E",  # 灰色
        })
        self.precisionPie.set_data(data)
        self.pieLayout.addWidget(self.precisionPie)

        self.recallPie = PieChartWidget(self.pieOkNgHost)
        self.recallPie.set_title("召回率：--%")
        self.recallPie.set_color_map({
            "OK": "#9E9E9E",  # 灰色
            "NG": "#4CAF50",  # 绿色
        })
        self.recallPie.set_data(data)
        self.pieLayout.addWidget(self.recallPie)

    def _update_pie_chart(self, sum_num, cost_time, ok_ok, ok_ng, ng_ok, ng_ng):
        """更新包括饼图在内的综合指标数据"""
        precision = round(ok_ok / (ok_ok + ok_ng) * 100, 1) if ok_ok + ok_ng > 0 else 0
        recall = round(ng_ng / (ng_ng + ng_ok) * 100, 1) if ng_ng + ng_ok > 0 else 0
        f1 = round(2 * ok_ok * 100 / (2 * ok_ok + ok_ng + ng_ok), 1) if ok_ok + ok_ng + ng_ok > 0 else 0
        avg_cost_time = round(cost_time / sum_num, 2)
        all_cost_time = round(cost_time / 1000, 2)

        self.f1Lab.setText(f"{f1}%")
        self.detectTimeLab.setText(f"{avg_cost_time}ms")
        self.sumImgLab.setText(f"{sum_num}")
        self.costTimeLab.setText(f"{all_cost_time}s")

        self.precisionPie.set_title(f"精确率：{precision}%")
        self.precisionPie.set_data({"OK": ok_ok, "NG": ok_ng})
        self.recallPie.set_title(f"召回率：{recall}%")
        self.recallPie.set_data({"OK": ng_ok, "NG": len(self.ng_false)})

    def _init_matrix(self):
        self.matrixWidget = MatrixWidget(self.cmGroupBox)
        self.verticalLayout_cm.addWidget(self.matrixWidget)

        self.matrixWidget.okGoodClicked.connect(lambda: self.handel_data(MATRIX.OKGOOD))
        self.matrixWidget.okBadClicked.connect(lambda: self.handel_data(MATRIX.OKBAD))
        self.matrixWidget.ngGoodClicked.connect(lambda: self.handel_data(MATRIX.NGGOOD))
        self.matrixWidget.ngBadClicked.connect(lambda: self.handel_data(MATRIX.NGBAD))

        self.matrixWidget.okSumClicked.connect(lambda: self.handel_data(MATRIX.OKSUM))
        self.matrixWidget.ngSumClicked.connect(lambda: self.handel_data(MATRIX.NGSUM))
        self.matrixWidget.preOkSumClicked.connect(lambda: self.handel_data(MATRIX.PREOKSUM))
        self.matrixWidget.preNgSumClicked.connect(lambda: self.handel_data(MATRIX.PRENGUM))

    def _init_score_histogram(self):
        self.scoreLayout = QVBoxLayout(self.scoreChartHost)
        self.scoreLayout.setContentsMargins(0, 0, 0, 0)
        self.scoreLayout.setSpacing(6)

        self.scoreHistogramWidget = HistogramThresholdWidget(self.scoreChartHost)
        self.scoreLayout.addWidget(self.scoreHistogramWidget)

        self.scoreHistogramWidget.attach_lists(self.ok_list, self.ng_list, poll_ms=200)
        self.scoreHistogramWidget.thresholdChanged.connect(self.handel_threshold)

    def _init_image_gallery(self):
        self.verticalLayout_images = QVBoxLayout(self.imageGroupBox)
        self.verticalLayout_images.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_images.setSpacing(6)

        self.imgWidget = ImgWidget(self.imageGroupBox)
        self.verticalLayout_images.addWidget(self.imgWidget)
        self.imgWidget.imageClicked.connect(self.handle_image_clicked)
        self.imgWidget.imgCvtButton.clicked.connect(self._toggle_converted_images)

    def handel_data(self, types):
        print("处理选中图片数据")
        selected = []
        match types:
            case MATRIX.OKGOOD:
                selected = self.ok_true
            case MATRIX.OKBAD:
                selected = self.ok_false
            case MATRIX.NGGOOD:
                selected = self.ng_true
            case MATRIX.NGBAD:
                selected = self.ng_false
            case MATRIX.OKSUM:
                selected = [*self.ok_true, *self.ok_false]
            case MATRIX.NGSUM:
                selected = [*self.ng_false, *self.ng_true]
            case MATRIX.PREOKSUM:
                selected = [*self.ok_true, *self.ng_true]
            case MATRIX.PRENGUM:
                selected = [*self.ok_false, *self.ng_false]
            case _:
                selected = []
        self.imgWidget.set_images(self._collect_images(selected))

    def _collect_images(self, results: List[AssessResult]):
        images = []
        for item in results:
            if item.img_path:
                images.append((item.img_path, item))
        return images

    def handel_threshold(self, value):
        print("阈值变化", value)
        self.threshold = value
        # 更新综合指标、混淆矩阵数据源
        self._update_data()

    def handle_image_clicked(self, detail: Optional[ImgDetailData]):
        print("选中图片结果:", detail)
        result = detail.datas
        tag = result.tag
        pre = "OK" if result.score < self.threshold else "NG"
        self.lblImageName.setText(os.path.basename(result.img_path))
        self.tagLab.setText(tag)
        self.lblPredValue.setText(pre)
        self.lblScoreValue.setText(str(result.score))
        self.lblStatusValue.setText("OK" if tag == pre else "NG")

    def _toggle_converted_images(self):
        self._show_converted_images = not self._show_converted_images
        self.imgWidget.set_show_converted(self._show_converted_images)
        if self._show_converted_images:
            self.imgWidget.imgCvtButton.setText("原图")
        else:
            self.imgWidget.imgCvtButton.setText("热图")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = AssessDialog()
    ui.show()
    sys.exit(app.exec())
