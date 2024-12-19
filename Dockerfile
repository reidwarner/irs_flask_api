FROM python:3.11.5-alpine

WORKDIR /IRS_FLASK_API

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "flask", "run", "--host=0.0.0.0", "--port=8080"]