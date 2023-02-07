from .airplane_core import AirplaneCore
from .http_layer import send_cmd, send_cmd_volatile
from enum import Enum
import json


class AirplaneModeEnum(Enum):
    """
    无人机airplane_mode函数设置飞行模式指令
    """
    CommonMode = 1
    MapMode = 2


class AirplaneController(AirplaneCore):
    """
    无人机控制
    此类包含控制单个无人机的所有指令
    """
    count: int = 1

    _send_cmd_fn = staticmethod(send_cmd)

    def use_fast_mode(self, enable=True):
        """
        是否使用非阻塞模式
        :param enable:
        :return:
        """
        if enable:
            # https://stackoverflow.com/questions/55527175/how-do-i-remove-implicit-passing-of-self-in-python-class
            _send_cmd_fn = staticmethod(send_cmd_volatile)
        else:
            _send_cmd_fn = staticmethod(send_cmd)
        pass

    def _next_count(self):
        self.count = self.count + 2
        return self.count

    def _prepare_command(self, json_obj: dict) -> str:
        json_obj['packageId'] = self._next_count()
        return json.dumps(json_obj)

    def _send_cmd(self, json_obj: dict) -> str:
        f = self._send_cmd_fn
        return f(self.keyName, self.CommandServiceHttpPort, self._prepare_command(json_obj), )

    def mode(self, mode: AirplaneModeEnum):
        """
        控制无人机飞行模式
        :param mode: 1,2,3,4
        :return:
        """
        self.airplane_mode(mode)
        pass

    def takeoff(self, high: int):
        """
        控制无人机起飞
        :param high: 起飞到指定高度
        :return:
        """
        return self._send_cmd({
            "cmdId": 11,
            "distance": high,
        })

    def land(self):
        """
        控制无人机降落
        """
        return self._send_cmd({
            "cmdId": 12,
        })

    def emergency(self):
        """停桨"""
        return self._send_cmd({
            "cmdId": 10,
        })

    def up(self, distance: int):
        """
        向上移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd({
            "cmdId": 13,
            "forward": 1,
            "distance": distance,
        })

    def down(self, distance: int):
        """
        向下移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd({
            "cmdId": 13,
            "forward": 2,
            "distance": distance,
        })

    def forward(self, distance: int):
        """
        The forward function moves the drone forward by a specified distance (meters).

        向前移动
        :param distance:移动距离（厘米）

        :param self: Access variables that belongs to the class
        :param distance:int: Specify the distance to move
        :return: The string &quot;ok&quot; if the command was successful
        :doc-author: Jeremie
        """
        return self._send_cmd({
            "cmdId": 13,
            "forward": 5,
            "distance": distance,
        })

    def back(self, distance: int):
        """
        向后移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd({
            "cmdId": 13,
            "forward": 6,
            "distance": distance,
        })

    def left(self, distance: int):
        """
        向左移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd({
            "cmdId": 13,
            "forward": 3,
            "distance": distance,
        })

    def right(self, distance: int):
        """
        向右移动
        :param distance:移动距离（厘米）
        """
        return self._send_cmd({
            "cmdId": 13,
            "forward": 4,
            "distance": distance,
        })

    def goto(self, x: int, y: int, h: int):
        """
        控制无人机到达指定位置
        :param x: x轴方向位置（厘米）
        :param y: y轴方向位置（厘米）
        :param h: 高度（厘米）
        """
        return self._send_cmd({
            "cmdId": 16,
            "x": x,
            "y": y,
            "h": h,
        })

    def flip(self, direction: str):
        """
        flip函数用于控制无人机翻滚
        :param direction: 翻滚方向（f前 b后 l左 r右）
        """
        raise Exception("flip not impl now.")
        # return self._send_cmd(f"flip {direction} 1")

    def flip_forward(self):
        """向前做翻转（翻跟头）动作
        """
        self.flip("f")
        pass

    def flip_back(self):
        """向后做翻转（翻跟头）动作
        """
        self.flip("b")
        pass

    def flip_left(self):
        """向左做翻转（翻跟头）动作
        """
        self.flip("l")
        pass

    def flip_right(self):
        """向右做翻转（翻跟头）动作
        """
        self.flip("r")
        pass

    def rotate(self, degree: int):
        """
        控制无人机旋转
        :param degree: 自转方向和角度（正数顺时针，负数逆时针，单位为度数）
        """
        if degree > 0:
            return self.cw(degree)
        else:
            return self.ccw(-degree)
        pass

    def cw(self, degree: int):
        """
        控制无人机顺时针自转
        :param degree: 自转角度度数
        """
        return self._send_cmd({
            "cmdId": 14,
            "rotate": 1,
            "rote": degree,
        })

    def ccw(self, degree: int):
        """
        控制无人机逆时针自转
        :param degree: 自转角度度数
        """
        return self._send_cmd({
            "cmdId": 14,
            "rotate": 2,
            "rote": degree,
        })

    def high(self, high: int):
        """
        控制无人机飞行高度
        :param high: 飞行到指定高度
        :return:
        """
        return self._send_cmd({
            "cmdId": 18,
            "high": high,
        })

    def speed(self, speed: int):
        """
        设置无人机飞行速度
        :param speed: 飞行速度（0-200厘米/秒）
        """
        return self._send_cmd({
            "cmdId": 19,
            "speed": speed,
        })

    def led(self, r: int, g: int, b: int):
        """
        控制无人机灯光为指定颜色
        :param r: 灯光颜色R通道
        :param g: 灯光颜色G通道
        :param b: 灯光颜色B通道
        """
        return self._send_cmd({
            "cmdId": 17,
            "ledMode": 1,
            "b": b,
            "g": g,
            "r": r,
        })

    def bln(self, r: int, g: int, b: int):
        """
        控制无人机灯光，呼吸灯
        :param r: 灯光颜色R通道
        :param g: 灯光颜色G通道
        :param b: 灯光颜色B通道
        """
        return self._send_cmd({
            "cmdId": 17,
            "ledMode": 2,
            "b": b,
            "g": g,
            "r": r,
        })

    def rainbow(self, r: int, g: int, b: int):
        """
        控制无人机灯光，七彩变换
        :param r: 灯光颜色R通道
        :param g: 灯光颜色G通道
        :param b: 灯光颜色B通道
        """
        return self._send_cmd({
            "cmdId": 17,
            "ledMode": 3,
            "b": b,
            "g": g,
            "r": r,
        })

    def airplane_mode(self, mode: AirplaneModeEnum):
        """
        设置无人机飞行模式
        :param mode: 1,2,3,4
        :return:
        """
        return self._send_cmd({
            "cmdId": 20,
            "flyMode": mode,
        })

    def stop(self):
        """
        控制无人机悬停
        """
        return self.hover()

    def hover(self):
        """
        控制无人机悬停
        """
        return self._send_cmd({
            "cmdId": 15,
        })

    pass
