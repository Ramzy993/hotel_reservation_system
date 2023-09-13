
FROM python:3.10-slim
RUN apt-get update
RUN apt-get install -y libpq-dev gcc
WORKDIR /opt/app
RUN python -m pip install --upgrade pip
COPY . /opt/app
RUN pip install -r /opt/app/requirments.txt
COPY ./requirments.txt /opt/app
ENV BUILD_TIMESTAMP=${TIMESTAMP}
EXPOSE 8008
CMD ["python3", "main.py"]
