# Test web-app to use with Pluralsight courses and Docker Deep Dive book
FROM python:3.12-slim

COPY pinger.py ./
COPY stats ./stats
ENV FLASK_APP=pinger.py
CMD ["python", "-u", "./pinger.py"]
