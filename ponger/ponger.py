from stats.server import StatsServer

ser = StatsServer("ponger", 8001)
ser.wait_loop()

