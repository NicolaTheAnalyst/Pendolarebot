FROM python:3.7-alpine
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /code
COPY main.py /code/
CMD ["python3", "main.py"]
