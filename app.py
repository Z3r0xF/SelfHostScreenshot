from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import threading
import os
import uuid
import time
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = FastAPI()
UPLOAD_FOLDER = './images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/images", StaticFiles(directory=UPLOAD_FOLDER), name="images")
 
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")


def delete_file_after_delay(filepath: str, delay: int):
    time.sleep(delay)
    os.remove(filepath)
    logging.info(f"Deleted file: {filepath}")


async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")


@app.post("/upload", dependencies=[Depends(verify_api_key)])
async def upload_file( file: UploadFile = File(...)):



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
