import socket
import time
from collections import deque
from random import randrange
import threading

class Balancer:
    def __init__(self, host, port, server_host, server_port):
        self.phost = host
        self.pport = port
        self.shost = server_host
        self.sport = server_port
        self.proxy = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.proxy.bind((self.phost, self.pport))
        self.serv_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def client_handler(self, data, cl_addr):
        delay = randrange(15)
        time.sleep(delay)
        self.serv_conn.sendto(data, (self.shost, self.sport))
        # Receive from server
        buf, addr = self.serv_conn.recvfrom(4096)
        self.proxy.sendto(buf, cl_addr)

    def proxy_server(self):
        print(f"Listening at {self.phost}:{self.pport}")
        while True:
            data, cl_addr = self.proxy.recvfrom(4096)
            new_cl = threading.Thread(target=self.client_handler, args=(data, cl_addr))
            new_cl.start()

if __name__ == "__main__":
    ser = Balancer("proxy1", 8080, "ponger", 8001)
    ser.proxy_server()

