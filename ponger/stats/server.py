import socket
import time
from collections import deque
from random import randrange

class StatsServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))

    def wait_loop(self):
        print("Staring echo-server")
        while True:
            data, cl_addr = self.server.recvfrom(4096)
            self.server.sendto(data, cl_addr)

if __name__ == "__main__":
    ser = StatsServer("ponger", 8001)
    ser.wait_loop()

