FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

RUN apt-get update

COPY requirements.txt .
RUN apt install git
RUN apt install git-lfs
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .

CMD python3 server.py
