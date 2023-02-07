"""
这个文件在 OwlControllerPython 库中负责解析从无人机发回的相机图像
"""
import cv2
import numpy as np
import io


# https://stackoverflow.com/questions/26509715/how-to-download-image-to-memory-using-python-requests
def parse_img(requestContent):
    """
    从仿真平台中返回的无人机相机图像是一个标准html编码的png/jpg图像
    本函数使用opencv的cv::imdecode函数将其解析为cv::Mat图像数据
    :param requestContent: 无人机相机图像数据 [TODO]
    :return: cv::Mat图像数据
    """
    im_arr = np.frombuffer(io.BytesIO(requestContent).getbuffer(), dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img
