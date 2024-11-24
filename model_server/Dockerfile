FROM huggingface/transformers-torch-light

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir /model

EXPOSE 8000

CMD [ "python3", "-u","app.py" ]

