import asyncio
import redis
import boto3
import logging
import cv_parser
import os
import json
from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_CHANNEL = "queue"

redis_client = redis.Redis(host='localhost', port=6379, db=0)

load_dotenv()
FILEBASE_ACCESS_KEY = os.getenv("FILEBASE_ACCESS_KEY")
FILEBASE_SECRET_KEY = os.getenv("FILEBASE_SECRET_KEY")
FILEBASE_BUCKET_NAME = os.getenv("FILEBASE_BUCKET_NAME")
FILEBASE_ENDPOINT_URL = os.getenv("FILEBASE_ENDPOINT_URL")

s3_client = boto3.client(
    's3',
    aws_access_key_id=FILEBASE_ACCESS_KEY,
    aws_secret_access_key=FILEBASE_SECRET_KEY,
    endpoint_url=FILEBASE_ENDPOINT_URL,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_file_from_filebase(cv_id):
    try:
        cv_file = s3_client.get_object(Bucket=FILEBASE_BUCKET_NAME, Key=cv_id)
        cv_text = cv_parser.extract_text_from_docx(cv_file['Body'].read())
        cv_json = cv_parser.convert_text_to_json(cv_text)

        json_filename = 'cv-processed/' + cv_id.split('/')[-1].replace('.docx', '.json')

        s3_client.put_object(Body=cv_json, Bucket=FILEBASE_BUCKET_NAME, Key=json_filename)

    except Exception as e:
        return None


def listen_to_queue():
    while True:
        cv_id = redis_client.brpop(REDIS_CHANNEL, timeout=0)
        if cv_id:
            cv_id = cv_id[1].decode()
            logger.info(f"Dequeued {cv_id}")
            extract_file_from_filebase(cv_id)


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, listen_to_queue)
    logger.info("Starting thread to listen to queue")


@app.get("/")
async def root():
    return {"message": "Running"}