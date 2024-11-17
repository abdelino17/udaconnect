FROM python:3.12-slim

WORKDIR .

RUN apt update && apt install -y build-essential python3-dev

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]