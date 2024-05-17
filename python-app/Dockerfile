FROM python:alpine

RUN apk add --no-cache postgresql-dev gcc musl-dev

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]