FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/src/app

WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

ADD . /usr/src/app

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
