import socket
import binascii
import struct
import threading
import json
from config import multicast_listen_port, multicast_listen_address, multicast_group_port, multicast_group_address, \
    multicast_additional_listen_address, multicast_additional_listen_port


# https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python

class MulticastManager(object):
    s: socket
    sl: socket

    tRecvNotice: threading.Thread
    tRecvResponse: threading.Thread

    stop = False

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        self.s.bind((multicast_listen_address, multicast_listen_port))
        host = socket.gethostbyname(socket.gethostname())
        self.s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
        mreq = struct.pack("4sl", socket.inet_aton(multicast_group_address), socket.INADDR_ANY)
        self.s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.sl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sl.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sl.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.sl.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        self.sl.bind((multicast_additional_listen_address, multicast_additional_listen_port))
        host = socket.gethostbyname(socket.gethostname())
        self.sl.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
        mreq = struct.pack("4sl", socket.inet_aton(multicast_group_address), socket.INADDR_ANY)
        self.sl.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.tRecvNotice = threading.Thread(target=self.recvNotice, )
        self.tRecvResponse = threading.Thread(target=self.recvResponse, )

        self.tRecvNotice.start()
        self.tRecvResponse.start()

        pass

    def recvNotice(self):
        while not self.stop:
            try:
                data, addr = self.s.recvfrom(1024)
            except socket.error as e:
                print('Exception')
            else:
                j = json.loads(data)
                if j['MultiCast'] == "Notice":
                    hexdata = binascii.hexlify(data)
                    print('Data data = %s' % data)
                    print('Data hexdata = %s' % hexdata)
                    print('Data j = %s' % j)
                    pass
                pass
            pass
        pass

    def recvResponse(self):
        while not self.stop:
            try:
                data, addr = self.sl.recvfrom(1024)
            except socket.error as e:
                print('Exception')
            else:
                j = json.loads(data)
                if j['MultiCast'] == "Response":
                    hexdata = binascii.hexlify(data)
                    print('sl Data data = %s' % data)
                    print('sl Data hexdata = %s' % hexdata)
                    print('sl Data j = %s' % j)
                    pass
                pass
            pass
        pass

    def sendQuery(self):
        self.sl.sendto(bytes('{"MultiCast":"Query"}', 'utf8'), (multicast_group_address, multicast_group_port))
        pass

    pass
