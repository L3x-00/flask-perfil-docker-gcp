import os
import datetime
from flask import Flask, render_template, request
from google.cloud import storage

app = Flask(__name__)

DEBUG = os.environ.get("DEBUG", "TRUE") == "TRUE"
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "my-gcs-bucket")

def get_storage_client():
    return storage.Client()

@app.route("/")
def home():
    return render_template('index.html', title='Equisd')

@app.route("/storage", methods=["GET", "POST"])
def storage_route():
    public_url = None
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                # Upload to GCS
                client = get_storage_client()
                bucket = client.bucket(GCS_BUCKET_NAME)
                blob = bucket.blob(file.filename)
                
                # Subir el archivo
                blob.upload_from_file(file)
                
                # Construir la URL pública estándar
                public_url = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{blob.name}"

    return render_template('storage.html', title='Equisd - Storage', signed_url=public_url)

if __name__ == "__main__":
    print(f"running debug as {DEBUG}")
    app.run(debug=DEBUG, host="0.0.0.0")
