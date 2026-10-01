#!/usr/bin/python3
from stats.client import StatsClient

mon = StatsClient([("proxy1", 8080), ("proxy2", 8081)])
mon.start()
