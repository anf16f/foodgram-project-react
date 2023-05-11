FROM python:3.9-slim

ENV SECRET_KEY="'django-insecure-+&of&##rvpc4ugjyo-l)v3p7g)45moj5hz9@%b89(t1no$bzm4'"

WORKDIR /app/api_foodgram

COPY . /app/api_foodgram

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r /app/api_foodgram/requirements.txt --no-cache-dir

CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000" ]