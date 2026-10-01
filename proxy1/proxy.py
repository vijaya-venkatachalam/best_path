from backend.balancer import Balancer

myproxy = Balancer("proxy1", 8080, "ponger", 8001)
myproxy.proxy_server()

