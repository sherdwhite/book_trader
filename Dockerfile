FROM python:3.11.2
WORKDIR /voltronflamingo/
ENV PYTHONPATH /voltronflamingo/
ENV DJANGO_SETTINGS_MODULE voltronflamingo.settings
COPY . /voltronflamingo/
RUN pip install -r /voltronflamingo/requirements.txt
