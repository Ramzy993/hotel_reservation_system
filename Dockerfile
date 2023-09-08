
FROM python:3.8-slim
WORKDIR /opt/app
RUN python -m pip install --upgrade pip
RUN apt-get update
COPY . /opt/app
RUN pip install --no-cache-dir -r /opt/app/requirments.txt
RUN mkdir output
ENV BUILD_TIMESTAMP=${TIMESTAMP}
EXPOSE 8008
CMD ["python3", "main.py"]
