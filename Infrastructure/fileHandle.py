from __future__ import annotations
import os
import shutil
import time
from pathlib import Path

import cv2


def check_path(path):
    Path(path).exists()
    raise FileNotFoundError(f"路径不存在: {path.resolve()}")


def clear_folder(folder):
    """
    清除 folder 文件夹内容
    :param
    :return:
    """
    if not os.path.isdir(folder):
        raise ValueError(f"文件夹 {folder} 不存在")

    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)  # 删除文件或符号链接
        else:
            shutil.rmtree(item_path)  # 删除子文件夹


def is_directory_stable(folder, interval=0.2, repeat=3):
    """
    用于判断文件夹中是否还有文件在写入
    返回 True：目录中所有文件稳定（大小不再变化）
    返回 False：仍有文件在写入
    """

    def snapshot():
        # 返回 {filepath: size} 字典
        return {
            f: os.path.getsize(os.path.join(folder, f))
            for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        }

    last = snapshot()

    for _ in range(repeat):
        time.sleep(interval)
        now = snapshot()
        if now != last:
            return False
        last = now

    return True


def load_images_from_folder(folder):
    """
    返回 folder 中所有图片的图片名列表，图片列表
    :param
    :return: img_list, name_list
    """
    img_list = []  # 存储 cv2.imread 读出的图像（numpy 数组）
    name_list = []  # 存储文件名（xxx.jpg
    if is_directory_stable(folder):
        for filename in os.listdir(folder):
            if filename.lower().endswith((".jpg", ".png", ".bmp", ".jpeg")):
                full_path = os.path.join(folder, filename)
                img = cv2.imread(full_path, cv2.IMREAD_COLOR)
                if img is not None:
                    img_list.append(img)
                    name_list.append(filename)
    return name_list, img_list


def save_mat_to_folder(mat, save_path):
    # 创建目标文件夹
    os.makedirs(save_path, exist_ok=True)

    filename = time.strftime("%Y%m%d_%H%M%S") + ".jpg"

    # 保存 JPG
    save_path = os.path.join(save_path, filename)
    success = cv2.imwrite(save_path, mat, [cv2.IMWRITE_JPEG_QUALITY, 100])

    if not success:
        raise Exception(f"保存失败：文件 {filename} 保存至 {save_path} 失败")
    print("save_mat_to_folder", save_path)
    return save_path


def copy_file_to_folder(path, folder):
    source = Path(path) if path else None
    if source and source.is_file():
        template_target = folder / source.name
        shutil.copy2(source, template_target)
        return str(template_target)
    return None
