FROM python:3.12-slim

WORKDIR /app

COPY app.py .
COPY test_app.py .

EXPOSE 8080

CMD ["python", "app.py"]
