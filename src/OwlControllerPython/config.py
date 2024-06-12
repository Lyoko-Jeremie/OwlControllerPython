"""
此文件编码了 全局配置信息
"""

remote_CommandServiceHttpPort = 23338
remote_ImageServiceHttpPort = 23331

http_retry_times = 10
http_timeout_cmd_connect = 1
http_timeout_cmd_read = 10


multicast_group_address = "239.255.0.1"
multicast_group_port = 30003
multicast_listen_address = "0.0.0.0"
multicast_listen_port = 30003

multicast_additional_listen_address = "0.0.0.0"
multicast_additional_listen_port = 30001
