from typing import Dict, Optional
from time import sleep
from random import randrange

from .control_command import AirplaneControllerExtended


class AirplaneManager(object):
    """
    管理并更新所有飞机状态的管理器
    """
    airplanes_table: Dict[str, AirplaneControllerExtended] = {}

    _client_id: int

    def __init__(self):
        self._client_id = randrange(110, 6553600)
        pass

    def ping(self):
        """
        这个函数为了完全适配PhantasyIslandPythonRemoteControl的API而存在
        """
        return {'ok': True, 'r': ''}

    def ping_volatile(self):
        """
        这个函数为了完全适配PhantasyIslandPythonRemoteControl的API而存在
        """
        return {'ok': True, 'r': ''}

    def start(self):
        """
        这个函数为了完全适配PhantasyIslandPythonRemoteControl的API而存在
        """
        self.flush()
        return {'ok': True, 'r': ''}

    def start_volatile(self):
        """
        这个函数为了完全适配PhantasyIslandPythonRemoteControl的API而存在
        """
        return {'ok': True, 'r': ''}

    def get_airplane(self, keyName: str) -> Optional[AirplaneControllerExtended]:
        """
        获取指定无人机
        这个函数获取的API完全适配PhantasyIslandPythonRemoteControl的API
        """
        a: Optional[AirplaneControllerExtended] = self.airplanes_table.get(keyName)
        if a is None:
            self.airplanes_table[keyName] = AirplaneControllerExtended(keyName, self._client_id)
            pass
        return self.airplanes_table.get(keyName)
        pass

    def get_airplane_extended(self, keyName: str) -> Optional[AirplaneControllerExtended]:
        """
        获取扩展飞机对象
        这个函数获取的API在完全适配PhantasyIslandPythonRemoteControl的API基础上，添加了FH0A无人机特有功能API
        :param keyName: 无人机的 keyName
        :return: AirplaneController
        """
        a = self.airplanes_table.get(keyName)
        if a is not None:
            return a
        else:
            self.airplanes_table[keyName] = AirplaneControllerExtended(keyName, self._client_id)
            return self.airplanes_table.get(keyName)
        pass

    def sleep(self, time):
        sleep(time)
        pass

    def flush(self):
        """
        更新当前管理器所管理的所有飞机的状态
        """
        for k, a in self.airplanes_table.items():
            a.flush()
            pass
        return None

    def destroy(self):
        """反注册所有无人机"""
        for i in self.airplanes_table.values():
            i.shutdown()
            pass
        self.airplanes_table = {}
        pass


airplane_manager_singleton = AirplaneManager()


def get_airplane_manager():
    """
    AirplaneManager是以单例模式工作的，故而需要使用这个函数来获取AirplaneManager单例对象
    :return: AirplaneManager单例对象
    """
    return airplane_manager_singleton
