FROM python:3.7

WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
ENTRYPOINT exec gunicorn -b 0.0.0.0:8080 dash-app.app:server