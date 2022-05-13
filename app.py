import numpy as np
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile , Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract 
import cv2
import config
from load import ImageProcessing
from starlette.responses import Response
import boto3
from datetime import datetime


app = FastAPI()

origins = [
    "http://localhost:8001", 
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load=ImageProcessing()

client_s3 = boto3.client( 
        's3', 
        region_name = config.AWS_S3_CONFIG['AWS_REGION'],
        aws_access_key_id = config.AWS_S3_CONFIG['AWS_ACCESS_KEY_ID'], 
        aws_secret_access_key = config.AWS_S3_CONFIG['AWS_SECRET_ACCESS_KEY']
)


@app.get("/")
async def read_root():
    return {"Health": "active"}


#OCR 인식 Request
@app.post("/ocr/")
async def upload_image(
    imagez: UploadFile = File(...),
    id:  int = Form(...),
    name: str = Form(...),
    ):
    try:
        image = Image.open(imagez.file)
        img = np.array(image)
        result = load.scanId(img,id,name)
        if result == -1:
            return JSONResponse(status_code=404)
        else:
            #res=client_s3.upload_file(imagez.file , config.AWS_S3_CONFIG['AWS_S3_BUCKET_NAME'], ExtraArgs={'ACL': 'public-read'} )
            #print(res)
            return {'url':'http://naver.com' } 
    except Exception as e:
        print('POST /image error: %e' % type(e))
        return JSONResponse(status_code=500,detail=e)
