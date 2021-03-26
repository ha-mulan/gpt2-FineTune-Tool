FROM python:3.7

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

RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install bs4
WORKDIR /app
COPY . .

CMD python3 server.py
