FROM python:3.14.6-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000:8000
CMD ["python", "main.py"]
