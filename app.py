from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import threading
import os
import uuid
import time
import logging
import magic
import mimetypes


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = FastAPI()
UPLOAD_FOLDER = './images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/images", StaticFiles(directory=UPLOAD_FOLDER), name="images")
 
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/x-msvideo', 'video/x-flv'}


def delete_file_after_delay(filepath: str, delay: int):
    time.sleep(delay)
    os.remove(filepath)
    logging.info(f"Deleted file: {filepath}")


async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")


def validate_file_type(file: UploadFile):

    file_content = file.file.read(1024)  # Read bytes from the beginning of the file
    file.file.seek(0)  # Reset the file cursor back to the beginning

    # Magic library to detect the file type
    mime_type = magic.from_buffer(file_content, mime=True)

    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type. Allowed types: JPG, PNG, GIF, MP4, AVI, FLV.")

@app.post("/upload", dependencies=[Depends(verify_api_key)])
async def upload_file( file: UploadFile = File(...)):

    validate_file_type(file)  # Validate file type

    # Generate a unique filename and respect the image format
    new_filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    file_location = os.path.join(UPLOAD_FOLDER, new_filename)

    # Save the uploaded file
    with open(file_location, "wb") as f:
        f.write(await file.read())


    #Default value is 0
    DELETE_TIME_MINUTES = os.getenv("DELETE_TIME_MINUTES")

    if int(DELETE_TIME_MINUTES) > 0:
        logging.info(f"Deleting file: {file_location} in {DELETE_TIME_MINUTES} minutes")
        #Convert seconds to minutes
        DELETE_TIME_MINUTES = int(DELETE_TIME_MINUTES) * 60
        threading.Thread(target=delete_file_after_delay, args=(file_location, DELETE_TIME_MINUTES)).start()

    # Generate a link to the uploaded file
    return {
        "info": f"File '{new_filename}' uploaded successfully.",
        "link": f"/images/{new_filename}"
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
