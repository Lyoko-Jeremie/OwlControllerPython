from .airplane_core import AirplaneCore, make_AirplaneFlyStatus
from .http_layer import send_cmd, send_cmd_volatile, get_airplane_status, sync_time
from enum import IntEnum
import json
import threading
from time import sleep


class AirplaneModeEnum(IntEnum):
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

    _can_use_resend_mode = False

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

    def __init__(self, keyName: str):
        super().__init__()
        self.keyName = keyName
        pass

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
            "cmdId": 120,
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
            "flyMode": mode.value,
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


class AirplaneControllerExtended(AirplaneController):
    """
    此类在AirplaneController的基础上添加了Owl特有的功能及函数
    """

    _resend_thread: threading.Thread = None
    _resend_shutdown = False
    _resend_last_cmd_json = None
    _client_id: int

    def __init__(self, keyName: str, client_id: int):
        super().__init__(keyName)
        self._client_id = client_id
        _resend_thread = threading.Thread(target=self._resend_thread_do, args=(self,))
        _resend_thread.start()
        pass

    def _resend_thread_do(self):
        while self._resend_shutdown is True:
            sleep(0.3)
            self._send_cmd_fn(
                self.keyName, self.CommandServiceHttpPort, self._resend_last_cmd_json,
                http_retry_times_=0,
                http_timeout_cmd_connect_=(0, 1), )
        pass

    def _send_cmd(self, json_obj: dict) -> str:
        f = self._send_cmd_fn
        p = self._prepare_command(self.json_obj)
        f = self._send_cmd_fn
        if json_obj["cmdId"] != 0:
            self._resend_last_cmd_json = p
            return f(self.keyName, self.CommandServiceHttpPort, p, )
        return f(self.keyName, self.CommandServiceHttpPort, p, )

    def ping(self):
        """
        ping
        """
        (r, j) = self._send_cmd({
            "cmdId": 0,
        })
        self._can_use_resend_mode = j["Version"] is not None
        return r

    def shutdown(self):
        self._resend_shutdown = True
        pass

    def flush(self):
        try:
            sync_time(self.keyName, self.ImageServiceHttpPort)
            self.status = make_AirplaneFlyStatus(get_airplane_status(self.keyName, self.CommandServiceHttpPort))
            pass
        except:
            # ignore
            pass
        pass

    def takeoff(self, high: int):
        self.ping()
        super().takeoff(high)
        pass

    def sleep(self, time):
        sleep(time)
        pass

    def __getattr__(self, item):
        """
        此函数为方法拦截器，
        用来拦截对此对象的不存在的函数的获取和调用，
        为了对其他库实现的适配而存在
        from https://stackoverflow.com/questions/14612442/how-to-handle-return-both-properties-and-functions-missing-in-a-python-class-u
        """

        def func(*arg, **kwargs):
            print("AirplaneControllerExtended __getattr__ placement")
            return None

        return func

    def get_cameraFrontTimestamp(self):
        return self.cameraFrontTimestamp
        pass

    def get_cameraDownTimestamp(self):
        return self.cameraDownTimestamp
        pass

    def calibrate(self):
        """

        """
        return self._send_cmd({
            "cmdId": 90,
        })

    pass
