FROM python:3.12

WORKDIR /

COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

ENV PORT=8000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
