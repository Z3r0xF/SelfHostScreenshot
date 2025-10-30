FROM python:3.14-slim

WORKDIR /app

ENV API_KEY=${API_KEY}
ENV DELETE_TIME_MINUTES=${DELETE_TIME_MINUTES}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
