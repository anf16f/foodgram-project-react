FROM python:3.9-slim

WORKDIR /app/api_foodgram

COPY . /app/api_foodgram

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r /app/api_foodgram/requirements.txt --no-cache-dir

CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000" ]