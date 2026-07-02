FROM python:latest

ENV DEBUG FALSE
ENV GCS_BUCKET_NAME my-gcs-bucket

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]