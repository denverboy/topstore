FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/topstore_project

CMD ["gunicorn", "topstore.wsgi:application", "--bind", "0.0.0.0:8000"]

