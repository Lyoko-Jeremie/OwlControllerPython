"""
这个文件是 PhantasyIslandPythonRemoteControl 库与仿真平台的核心通信协议部分
"""
from typing import Dict
import sys

import requests
import json


# def ping(target: str, port: int):
#     return send_cmd(target, port, 'ping')


# def ping_volatile(target: str, port: int):
#     return send_cmd_volatile(target, port, 'ping')


# def start(target: str, port: int):
#     return send_cmd(target, port, 'start')


# def start_volatile(target: str, port: int):
#     return send_cmd_volatile(target, port, 'start')


def send_get_camera(target: str, port: int, camera_id: int | str):
    try:
        r = requests.get('http://' + target + str(port) + '/' + str(camera_id), timeout=3)
        if r.status_code != 200:
            return None
        return r.content
    except requests.exceptions.ReadTimeout as e:
        return None
    except requests.exceptions.ConnectionError as e:
        return None


def send_cmd(target: str, port: int, jsonS: str):
    try:
        r = requests.post('http://' + target + str(port) + '/ECU_HTTP/cmd', data=jsonS, timeout=3)
        print(r.status_code)
        if r.status_code != 200:
            return {'ok': False, 'r': 'status_code'}
        print(r.text)
        j = json.loads(r.text)
        print(j)
        return (j['ok'], j['r'])
    except requests.exceptions.ReadTimeout as e:
        print('send_cmd ', jsonS, ' ', 'Error Command Timeout')
        return {'ok': False, 'r': 'Timeout'}
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError Cannot Connect to Airplane, Max retries exceeded.', file=sys.stderr)
        try:
            print('  ===>>>  ' + str(e.args[0].reason), file=sys.stderr)
        except:
            pass
        return {'ok': False, 'r': 'ConnectionError Cannot Connect to Airplane'}


def send_cmd_volatile(target: str, port: int, jsonS: str):
    try:
        r = requests.post('http://' + target + str(port) + '/ECU_HTTP/cmd', data=jsonS, timeout=3)
        print(r.status_code)
        if r.status_code != 200:
            return {'ok': False, 'r': 'status_code'}
        print(r.text)
        j = json.loads(r.text)
        return (j['ok'], j['r'])
    except requests.exceptions.ReadTimeout as e:
        print('send_cmd_volatile ', jsonS, ' ', 'Error Command Timeout')
        return {'ok': False, 'r': 'Timeout'}
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError Cannot Connect to Airplane, Max retries exceeded.', file=sys.stderr)
        try:
            print('  ===>>>  ' + str(e.args[0].reason), file=sys.stderr)
        except:
            pass
        return {'ok': False, 'r': 'ConnectionError Cannot Connect to Airplane'}


# def get_all_airplane_status(target: str):
#     # error = None
#     # try:
#     #     r = requests.get('http://' + target + '/ECU_HTTP/getAllAirplaneStatus', timeout=5)
#     #     # print(r.status_code)
#     #     j = json.loads(r.text)
#     #     return j
#     # except requests.exceptions.ConnectionError as e:
#     #     print('ConnectionError Cannot Connect to PhantasyIsland, Max retries exceeded.', file=sys.stderr)
#     #     try:
#     #         print('  ===>>>  ' + str(e.args[0].reason), file=sys.stderr)
#     #     except:
#     #         print(e, file=sys.stderr)
#     #     error = e
#     #     pass
#     # if error is not None:
#     #     raise Exception('ConnectionError Cannot Connect to PhantasyIsland, Max retries exceeded.')
#     pass


def process_airplane(j: Dict[str, any]):
    if j['ok'] is True:
        airplanes = j['airplanes']
        # print(airplanes)
        airplaneStatus: Dict[str, Dict[str, any]] = {}
        for air in airplanes:
            # print(air)
            status: Dict[str, any] = {}
            # print(air['keyName'])
            # print(air['typeName'])
            # print(air['updateTimestamp'])
            # print(air['status'])
            status['keyName'] = air['keyName']
            status['typeName'] = air['typeName']
            status['updateTimestamp'] = air['updateTimestamp']
            status['status'] = air['status']
            # print(air['cameraDown'])
            # print(air['cameraFront'])
            camera_front = air['cameraFront']
            camera_front_img_data_string = camera_front['imgDataString']
            status['cameraFront'] = camera_front_img_data_string
            camera_down = air['cameraDown']
            camera_down_img_data_string = camera_down['imgDataString']
            status['cameraDown'] = camera_down_img_data_string
            # # print(cameraFront['imgDataString'])
            # img = read_b64_img(cameraFront['imgDataString'])
            # # print(img)
            # if img is not None:
            #     cv2.imshow(air['keyName'], img)
            #     cv2.waitKey(1)
            # else:
            #     print(img)
            # pass
            airplaneStatus[status['keyName']] = status
            pass
        return airplaneStatus
    else:
        return None
    pass
