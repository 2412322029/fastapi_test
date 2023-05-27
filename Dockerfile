FROM python:3.10-buster

WORKDIR /code

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY ./ /code/

RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable

CMD python app.py