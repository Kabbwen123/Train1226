# patchcore_debug_utils.py
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import cv2
import torch

try:
    import faiss
except Exception:
    faiss = None


def img_md5_bgr(img_bgr: np.ndarray) -> str:
    """用像素字节计算 md5：可用来判断 cv2/PIL 解码是否真的一致。"""
    h = hashlib.md5()
    h.update(img_bgr.tobytes())
    return h.hexdigest()


def faiss_index_info(index: Any) -> Dict[str, Any]:
    """尽量提取：type / is_gpu / ntotal / d / nprobe / efSearch。"""
    if index is None:
        return {"exists": False}

    tname = type(index).__name__
    info: Dict[str, Any] = {
        "exists": True,
        "py_type": tname,
        "is_gpu": ("Gpu" in tname) or ("gpu" in tname.lower()),
    }

    for attr in ("ntotal", "d", "is_trained"):
        try:
            info[attr] = getattr(index, attr)
        except Exception:
            pass

    # IVF nprobe
    try:
        if hasattr(index, "nprobe"):
            info["nprobe"] = int(index.nprobe)
    except Exception:
        pass

    # HNSW efSearch
    try:
        if hasattr(index, "hnsw") and hasattr(index.hnsw, "efSearch"):
            info["efSearch"] = int(index.hnsw.efSearch)
    except Exception:
        pass

    # 粗略 kind
    low = tname.lower()
    if "hnsw" in low:
        info["kind"] = "HNSW"
    elif "ivf" in low:
        info["kind"] = "IVF"
    elif "pq" in low:
        info["kind"] = "PQ"
    elif "flat" in low:
        info["kind"] = "Flat"
    else:
        info["kind"] = "Unknown"

    return info


def runtime_env_info() -> Dict[str, Any]:
    d: Dict[str, Any] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "opencv": cv2.__version__,
        "torch": torch.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
        "cuda_device_count": int(torch.cuda.device_count()) if torch.cuda.is_available() else 0,
    }
    if faiss is not None:
        d["faiss"] = getattr(faiss, "__version__", "unknown")
        try:
            d["faiss_gpu_count"] = int(faiss.get_num_gpus())
        except Exception:
            d["faiss_gpu_count"] = None
    else:
        d["faiss"] = "not_imported"
        d["faiss_gpu_count"] = None
    return d


def dump_json(path: str | Path, obj: Dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def save_npy(path: str | Path, arr: Optional[np.ndarray]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if arr is None:
        return
    np.save(str(path), arr)


def debug_print_runtime(title: str, index: Any, extra: Dict[str, Any]) -> None:
    """load 后打印一组关键一致性信息。"""
    print(f"\n========== [PatchCore DEBUG] {title} ==========")
    info = faiss_index_info(index)
    print("[Faiss] ", info)
    for k, v in extra.items():
        print(f"[{k}] {v}")
    print("=============================================\n")
