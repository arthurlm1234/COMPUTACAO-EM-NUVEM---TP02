FROM python:latest

RUN pip install mlxtend pandas

WORKDIR /app
COPY . /app

CMD ["python", "ml_trainer.py"]