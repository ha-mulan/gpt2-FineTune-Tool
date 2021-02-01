FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

RUN apt-get update

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get install -y g++
RUN pip install spacy
RUN pip install unidecode
RUN pip install word2number
RUN pip install contractions
RUN pip install inflect
RUN pip install nltk

WORKDIR /app
COPY . .

CMD python3 server.py
