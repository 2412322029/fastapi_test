FROM python:3.10-buster

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 config  set global.index-url http://mirrors.aliyun.com/pypi/simple/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/

CMD python app.py