# Basic flask container

FROM fanoftal2/flask-crud-base:1


ADD ./app /home/app/
WORKDIR /home/app/

COPY .env /home/app/.env

COPY requirements.txt /home/app/requirements.txt

RUN apk add --no-cache postgresql-dev gcc python3 python3-dev musl-dev && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip3 install -r requirements.txt





EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]
