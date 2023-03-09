"""
这个文件是 PhantasyIslandPythonRemoteControl 库与仿真平台的核心通信协议部分
"""
from typing import Dict
import sys
import datetime

import requests
from requests.adapters import HTTPAdapter, Retry
import json
from .config import http_retry_times, http_timeout_cmd_connect, http_timeout_cmd_read


# def ping(target: str, port: int):
#     return send_cmd(target, port, 'ping')


# def ping_volatile(target: str, port: int):
#     return send_cmd_volatile(target, port, 'ping')


# def start(target: str, port: int):
#     return send_cmd(target, port, 'start')


# def start_volatile(target: str, port: int):
#     return send_cmd_volatile(target, port, 'start')


def send_get_camera(target: str, port: int, camera_id: str):
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=http_retry_times))
        r = s.get('http://' + target + ':' + str(port) + '/' + str(camera_id), timeout=(3, 2))
        if r.status_code != 200:
            return None
        r.headers["X-image-height"]
        r.headers["X-image-width"]
        r.headers["X-image-pixel-channel"]
        r.headers["X-image-format"]
        r.headers["X-SteadyClockTimestampMs"]
        return r
    except requests.exceptions.ReadTimeout as e:
        return None
    except requests.exceptions.ConnectionError as e:
        return None


def sync_time(target: str, port: int):
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=http_retry_times))
        r = s.get(
            'http://' + target + ':' + str(port) + '/time?setTimestamp=' + str(datetime.datetime.now().timestamp()),
            timeout=1)
        if r.status_code != 200:
            return None
        j = json.loads(r.text)
        print(j)
        return datetime.datetime.fromtimestamp(int(j["steadyClockTimestampMs"]))
    except requests.exceptions.ReadTimeout as e:
        # print("sync_time except requests.exceptions.ReadTimeout")
        return None
    except requests.exceptions.ConnectTimeout as e:
        # print("sync_time except requests.exceptions.ConnectTimeout")
        return None
    except requests.exceptions.ConnectionError as e:
        # print("sync_time except requests.exceptions.ConnectionError")
        return None
    pass


def send_cmd(target: str, port: int, jsonS: str):
    try:
        # https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=http_retry_times))
        r = s.post('http://' + target + ':' + str(port) + '/cmd', data=jsonS,
                   timeout=(http_timeout_cmd_connect, http_timeout_cmd_read))
        print(r.status_code)
        if r.status_code != 200:
            return {'ok': False, 'r': 'status_code'}
        print(r.text)
        j = json.loads(r.text)
        print(j)
        return (j['result'])
    except requests.exceptions.ReadTimeout as e:
        print('send_cmd ', jsonS, ' ', 'Error Command ReadTimeout')
        return {'ok': False, 'r': 'Timeout'}
    except requests.exceptions.ConnectTimeout as e:
        print('send_cmd ', jsonS, ' ', 'Error Command ConnectTimeout')
        return {'ok': False, 'r': 'Timeout'}
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError Cannot Connect to Airplane, Max retries exceeded.', jsonS, file=sys.stderr)
        try:
            print('  ===>>>  ' + str(e.args[0].reason), file=sys.stderr)
        except:
            pass
        return {'ok': False, 'r': 'ConnectionError Cannot Connect to Airplane'}


def send_cmd_volatile(target: str, port: int, jsonS: str):
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=http_retry_times))
        r = s.post('http://' + target + ':' + str(port) + '/cmd', data=jsonS,
                   timeout=(http_timeout_cmd_connect, http_timeout_cmd_read))
        print(r.status_code)
        if r.status_code != 200:
            return {'ok': False, 'r': 'status_code'}
        print(r.text)
        j = json.loads(r.text)
        return (j['result'])
    except requests.exceptions.ReadTimeout as e:
        print('send_cmd_volatile ', jsonS, ' ', 'Error Command ReadTimeout')
        return {'ok': False, 'r': 'Timeout'}
    except requests.exceptions.ConnectTimeout as e:
        print('send_cmd_volatile ', jsonS, ' ', 'Error Command ConnectTimeout')
        return {'ok': False, 'r': 'Timeout'}
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError Cannot Connect to Airplane, Max retries exceeded.', jsonS, file=sys.stderr)
        try:
            print('  ===>>>  ' + str(e.args[0].reason), file=sys.stderr)
        except:
            pass
        return {'ok': False, 'r': 'ConnectionError Cannot Connect to Airplane'}


def get_airplane_status(target: str, port: int):
    error = None
    try:
        r = requests.get('http://' + target + ':' + str(port) + '/AirplaneState', timeout=1)
        # print(r.status_code)
        j = json.loads(r.text)
        return process_airplane(j)
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError Cannot Connect to airplane, Max retries exceeded.', file=sys.stderr)
        try:
            print('  ===>>>  ' + str(e.args[0].reason), file=sys.stderr)
        except:
            print(e, file=sys.stderr)
        error = e
        pass
    if error is not None:
        raise Exception('ConnectionError Cannot Connect to airplane, Max retries exceeded.')
    pass


def process_airplane(j: Dict[str, any]):
    if j['result'] is True:
        air = j['state']
        tag = j['tag']
        status: Dict[str, any] = {}
        status['timestamp'] = air['timestamp']
        status['stateFly'] = air['stateFly']
        status['pitch'] = air['pitch']
        status['roll'] = air['roll']
        status['yaw'] = air['yaw']
        status['vx'] = air['vx']
        status['vy'] = air['vy']
        status['vz'] = air['vz']
        status['high'] = air['high']
        status['tag_ok'] = tag['ok']
        status['tag_x'] = tag['x']
        status['tag_y'] = tag['y']
        status['tag_z'] = tag['z']
        status['nowTimestampSteady'] = j['nowTimestamp']
        status['nowTimestampSystem'] = j['nowTimestampC']
        print(status)
        return status
    else:
        return None
    pass
