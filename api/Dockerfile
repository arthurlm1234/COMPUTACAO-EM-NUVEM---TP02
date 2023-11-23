FROM python:latest

RUN pip install flask pandas

COPY api.py /app/api.py
WORKDIR /app

EXPOSE 32171

CMD ["python", "api.py", "--host=0.0.0.0"]