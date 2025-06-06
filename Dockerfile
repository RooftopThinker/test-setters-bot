FROM python:3.12

WORKDIR /bot

COPY requirements.txt .
COPY ./ .

RUN pip install -r requirements.txt


CMD ["python", "./main.py"]