import psutil


def getcpumsg():
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    # net = psutil.net_io_counters()
    return {
        'cpu': cpu,
        'memory': {
            'total': memory.total,  # 总物理内存
            'used': memory.used,  # 可用
        },
        # 'io': {
        #     'bytes_sent': net.bytes_sent,  # 发送的字节数
        #     'bytes_recv': net.bytes_recv,  # 接收的字节数
        #     'packets_sent': net.packets_sent,  # 发送的数据包数
        #     'packets_recv': net.packets_recv  # 接收的数据包数
        # }
    }


def getdisk():
    disk = psutil.disk_usage('/')
    return {
        'disk': {
            'total': disk.total,
            'used': disk.used,
            'percent': disk.percent
        }
    }

