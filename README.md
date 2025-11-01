Screenshot Server with FastAPI

This repository contains a FastAPI application serving as a lightweight screenshot server. It allows you to upload screenshots and GIFs, which are stored temporarily and can be shared via generated links. Uploaded files are automatically deleted after a specified duration, definied by "DELETE_TIME_MINUTES".


File Upload Supports JPG, PNG, GIF, MP4, AVI, and FLV formats.
Temporary Storage: Files are stored based on a user-defined deletion time definied by DELETE_TIME_MINUTES.
API Key Authentication: Secures your uploads with API key access definied by API_KEY (Generate your custom key).

docker-compose.yml:


```
version: '3.8'

services:
  screenshot_server:
    image: z3r0xf/selfhostscreenshot:latest
    ports:
      - "7070:5000"
    environment:
      - API_KEY=XXXXX-XXXXXX-XXXXX-XXXXX # IMPORTANT: Generate your own key
      - DELETE_TIME_MINUTES=30
```
API Usage

You can upload a file using the following curl command:


```
curl -X POST https://YOURDOMAIN/upload \
  -H "X-API-Key: XXXXX-XXXXXX-XXXXX-XXXXX" \
  -F "file=@helloworld.jpg"
```
Response Example

The server responds with a JSON object similar to this:
```
{
    "info": "File 'helloworld.jpg' uploaded successfully.",
    "link": "/images/1dc4d2d9-8863-47e2-bd5c-b627c1ab478d.jpg"
}
```
Custom URL Sharing

Once the screenshot is uploaded, you can quickly share it via your custom URL.

It's up to you how you manage the response automatically:

https://YOURDOMAIN/images/1dc4d2d9-8863-47e2-bd5c-b627c1ab478d.jpg
