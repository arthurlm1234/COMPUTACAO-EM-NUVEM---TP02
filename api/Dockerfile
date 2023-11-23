FROM python:latest

RUN pip install flask pandas

WORKDIR /app
COPY . /app

EXPOSE 32171

CMD ["python", "api.py", "--host=0.0.0.0"]
#CMD ["cd /; ls -a"]