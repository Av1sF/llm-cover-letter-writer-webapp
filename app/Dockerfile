FROM python:3.12.0b1-slim-buster

WORKDIR /app 

COPY requirements.txt ./

RUN pip install -r requirements.txt 

COPY . .

EXPOSE 5000

CMD ["python", "-u", "app.py"]
