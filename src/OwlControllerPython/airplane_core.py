import dataclasses
from typing import Dict

import datetime

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


@dataclasses.dataclass()
class AirplaneFlyStatusExtended(AirplaneFlyStatus):
    vx: float
    vy: float
    vz: float
    nowTimestampSteady: datetime.datetime
    nowTimestampSystem: datetime.datetime
    timestamp: datetime.datetime
    pass


def make_AirplaneFlyStatus(
        fly_status: Dict[str, any]
) -> AirplaneFlyStatusExtended:
    return AirplaneFlyStatusExtended(
        landing=fly_status['stateFly'],  # ?
        isStop=fly_status['stateFly'],  # ?
        x=0,  # ?
        y=0,  # ?
        h=fly_status['high'],
        rX=fly_status['pitch'],  # ?
        rY=fly_status['yaw'],
        rZ=fly_status['roll'],  # ?
        vx=fly_status['vx'],
        vy=fly_status['vy'],
        vz=fly_status['vz'],
        nowTimestampSteady=datetime.datetime.utcfromtimestamp(fly_status['nowTimestampSteady'] / 1000),
        nowTimestampSystem=datetime.datetime.utcfromtimestamp(fly_status['nowTimestampSystem'] / 1000),
        timestamp=datetime.datetime.utcfromtimestamp(fly_status['timestamp'] / 1000),
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
    status: AirplaneFlyStatusExtended
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
