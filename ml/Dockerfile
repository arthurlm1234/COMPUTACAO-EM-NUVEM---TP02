FROM python:latest

RUN pip install mlxtend pandas

COPY ml_trainer.py /app/ml_trainer.py
WORKDIR /app

CMD ["python", "ml_trainer.py"]