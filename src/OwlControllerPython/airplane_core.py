import dataclasses
from typing import Dict

from .config import remote_CommandServiceHttpPort, remote_ImageServiceHttpPort
from .http_layer import send_get_camera
from .image_process import parse_img


@dataclasses.dataclass()
class AirplaneFlyStatus(object):
    """
    每个飞机的飞行状态
    """
    landing: bool
    isStop: bool
    x: float
    y: float
    h: float
    rX: float
    rY: float
    rZ: float
    pass


def make_AirplaneFlyStatus(
        fly_status: Dict[str, any]
):
    return AirplaneFlyStatus(
        landing=fly_status['landing'],
        isStop=fly_status['isStop'],
        x=fly_status['x'],
        y=fly_status['y'],
        h=fly_status['h'],
        rX=fly_status['rX'],
        rY=fly_status['rY'],
        rZ=fly_status['rZ'],
    )
    pass


@dataclasses.dataclass()
class AirplaneCore(object):
    """
    每个飞机的基本信息
    :var keyName
    """
    keyName: str
    typeName: str
    updateTimestamp: int
    status: AirplaneFlyStatus
    cameraFront: str
    cameraDown: str

    CommandServiceHttpPort: int
    ImageServiceHttpPort: int

    def __init__(self):
        self.CommandServiceHttpPort = remote_CommandServiceHttpPort
        self.ImageServiceHttpPort = remote_ImageServiceHttpPort

    def get_camera_front_img(self):
        """
        获取前置摄像头图像
        :return:  cv::Mat
        """
        r = send_get_camera(self.keyName, self.ImageServiceHttpPort, 'down')  # TODO
        if r is None:
            return
        return parse_img(r)
        pass

    def get_camera_down_img(self):
        """
        获取下置摄像头图像
        :return:  cv::Mat
        """
        r = send_get_camera(self.keyName, self.ImageServiceHttpPort, 'front')  # TODO
        if r is None:
            return
        return parse_img(r)
        pass

    pass
