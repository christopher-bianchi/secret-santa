FROM python:3

MAINTAINER Christopher Bianchi

WORKDIR /usr/src/app

ENV PYTHONPATH /usr/src/app

COPY santas.txt email_template.txt santa.py ./

CMD ["python", "santa.py"]
