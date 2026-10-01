import socket
import time
from collections import deque
import threading

def calculate_rtt(rtt_list):
    mean = 0
    total = 0
    for rtt in rtt_list:
        total = total + rtt

    if len(rtt_list):
        mean = total/len(rtt_list)
        return mean
    else:
        return 0xFFFFFFFF

class StatsGatherer:
    """Stats proxy class gets and stores the stats for a proxy"""
    def __init__(self, tcpaddr):
        self.host = tcpaddr[0]
        self.port = tcpaddr[1]
        self.rtt = deque([])
        self.mean = 0xFFFFFFFF
        print(f"Starting client to proxy {self.host}:{self.port}")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_proxy_stats(self):
        while True:
            epoch_time = int(time.time())
            time_str = str(epoch_time)
            self.client.sendto(time_str.encode(), (self.host, self.port))
            data, addr = self.client.recvfrom(4096)
            time_str = data.decode()
            rtt = int(time.time()) - int(time_str)
            # Pop entries from the front when new data is received, LIFO
            if (len(self.rtt) > 5):
                item = self.rtt.popleft()
            self.rtt.append(rtt)
            self.mean = calculate_rtt(self.rtt)
            print(f"Path metrics via {self.host}:{self.port}, rtt = {self.mean}s")
            time.sleep(1)

    def start(self):
        """ Start gathering RTT metrics """
        self.timer = threading.Timer(1, self.get_proxy_stats)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

class StatsClient:
    """ Get RTT stats by sending timestamp in an echo packet
    that the server (running at host, port) echoes back """
    def __init__(self, tcpaddr_list):
        self.proxy = []
        for tcpaddr_list in tcpaddr_list:
            proxy = StatsGatherer(tcpaddr_list)
            self.proxy.append(proxy)

    def dump_all_metrics(self):
        for proxy in self.proxy:
            print(f"proxy {proxy.host}:{proxy.port}, metrics = {proxy.mean}s")

    def find_best_path(self):
        while True:
            print("========== Metrics Report Start =============")
            self.dump_all_metrics()
            best_mean = 0xFFFFFFFF
            best_proxy = None
            for proxy in self.proxy:
                if best_mean >= proxy.mean:
                    best_proxy = proxy
                    best_mean = proxy.mean
            if best_proxy != None:
                print(f"Found best path {best_proxy.host}:{best_proxy.port}, metrics = {best_proxy.mean}s")
            else:
                print("Error finding best path")
            print("========== Metrics Report End =============")
            time.sleep(60)

    def start(self):
        for proxy in self.proxy:
            proxy.start()
        self.timer = threading.Timer(60, self.find_best_path)
        self.timer.start()

    def stop(self):
        for proxy in self.proxy:
            proxy.stop()
        self.timer.cancel()

if __name__ == "__main__":
    cl = StatsClient([("proxy1", 8080), ("proxy2", 8081)])
    cl.start()
