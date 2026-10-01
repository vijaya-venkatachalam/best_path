from backend.balancer import Balancer

myproxy = Balancer("proxy2", 8081, "ponger", 8001)
myproxy.proxy_server()

