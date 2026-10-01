# Test web-app to use with Pluralsight courses and Docker Deep Dive book
FROM python:3.12-slim

COPY proxy.py ./
COPY backend ./backend

CMD ["python", "-u", "./proxy.py"]
