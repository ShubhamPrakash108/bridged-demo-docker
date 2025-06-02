FROM python:3.9-slim

WORKDIR /app_fastapi

COPY . /app_fastapi

RUN pip install --no-cache-dir -r /app_fastapi/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
