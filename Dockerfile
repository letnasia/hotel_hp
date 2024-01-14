FROM python:3.11

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

# Install mysql and psql clients
RUN apt-get update && apt-get install -y mariadb-client postgresql-client

VOLUME [ "/app" ]

EXPOSE 8000

# Run the app:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
