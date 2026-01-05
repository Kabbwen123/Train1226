import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any


@dataclass
class Project:
    """项目配置的数据载体。"""

    def __init__(self, id, name, type, template_path, mask_path, create_time):
        self.id = int(id) if id is not None else None
        self.name = name
        self.type = int(type) if type is not None else None
        self.template_path = template_path
        self.mask_path = mask_path
        self.create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S") if create_time is not None else None

    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[int] = None
    template_path: Optional[str] = None
    mask_path: Optional[str] = None
    create_time: Optional[datetime] = None
    
class Image:
    """对齐裁剪的图片的数据载体。"""

    def __init__(self, id, project_id, name, path_convert, tag, subtag):
        self.id = int(id) if id is not None else None
        self.project_id = int(project_id) if project_id is not None else None
        self.name = name
        self.path_convert = path_convert
        self.tag = tag
        self.subtag = subtag

    id: Optional[int] = None
    project_id: Optional[int] = None
    name: Optional[str] = None
    path_convert: Optional[str] = None
    tag: Optional[str] = None
    subtag: Optional[str] = None


@dataclass
class Model:
    """模型信息的数据载体。"""

    def __init__(self, id, project_id, model_name, dataset, config, create_time, path):
        self.id = int(id) if id is not None else None
        self.project_id = int(project_id) if project_id is not None else None
        self.model_name = model_name
        self.dataset = self._parse_json(dataset)
        self.config = self._parse_json(config)
        self.create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S") if create_time is not None else None
        self.path = path

    @staticmethod
    def _parse_json(value: Any) -> Any:
        if value is None or value == "":
            return None
        if isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value

    id: Optional[int] = None
    project_id: Optional[int] = None
    model_name: Optional[str] = None
    dataset: Optional[Any] = None
    config: Optional[Any] = None
    create_time: Optional[datetime] = None
    path: Optional[str] = None


@dataclass
class AssessResult:
    def __init__(self, id, model_id, tag, label, score, img_path, img_path_cvt, defect_count, detect_time):
        self.id = int(id) if id is not None else None
        self.model_id = int(model_id) if model_id is not None else None
        self.tag = tag
        self.label = label
        self.score = float(score) if score is not None else None
        self.img_path = img_path
        self.img_path_cvt = img_path_cvt
        self.defect_count = defect_count
        self.detect_time = float(detect_time) if detect_time is not None else None

    def to_str(self):
        info = ""
        if self.id is not None:
            name = self.img_path_cvt.split("/")[-1]
            info += f"图像名称: {name}\n"
        if self.tag is not None:
            info += f"标签类别: {self.tag}\n"
        if self.label is not None and self.detect_time is not None:
            info += f"检测结果: {self.label}\n"
            info += f"检测耗时: {self.detect_time}\n"

    id: Optional[int] = None
    model_id: Optional[int] = None
    tag: Optional[int] = None
    label: Optional[str] = None
    score: Optional[float] = None
    img_path: Optional[str] = None
    img_path_cvt: Optional[str] = None
    defect_count: Optional[int] = None
    detect_time: Optional[datetime] = None


@dataclass
class ImgDetailData:
    def __init__(self, path, path_cvt, info, datas):
        self.path = path
        self.path_cvt = path_cvt
        self.info = info
        self.datas = datas

    path: Optional[str] = None
    path_cvt: Optional[str] = None
    info : Optional[str] = None
    datas: Optional[Any] = None  # 处理额外需要携带的数据
