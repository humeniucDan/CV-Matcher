import asyncio
import redis.asyncio as redis
import scripts.repo.filebase_repo as filebase
import scripts.service.cv_service as cv_service
import scripts.service.job_service as job_service

import scripts.util.json_parser as json_parser # delete after test

HOST, PORT = 'localhost', 6379
CV_QUEUE   = 'queue:cvs'
JOB_QUEUE  = 'queue:jobs'

async def listener(stop_event: asyncio.Event):
    client = redis.Redis(host=HOST, port=PORT, db=0)
    try:
        while not stop_event.is_set():
            result = await client.blpop([CV_QUEUE, JOB_QUEUE], timeout=1)
            if result:
                queue_name, raw = result
                if queue_name.decode() == CV_QUEUE:
                    await process_cv(raw)
                else:
                    await process_job(raw)
    finally:
        await client.aclose()

async def process_cv(data: bytes):
    try:
        file = f'cv-raw/{data.decode('utf-8')}'
        print("Process CV:", file)
        cv = filebase.get_object(file)
        cv_service.add_cvs(cv)
        #json = json_parser.summary_cv(cv)

        #file_insert = f'cv-processed/{data.decode('utf-8')}.json'
        #filebase.put_object(file_insert, json)
    except Exception as e:
        print(f"Error processing CV: {e}")

async def process_job(data: bytes):
    try:
        file = f'jobs/{data.decode('utf-8')}'
        print("Process Job:", file)
        job = filebase.get_object(file)
        job_service.add_jobs(job)

        #json = json_parser.summary_job(job)
        #print(json)

    except Exception as e:
        print(f"Error processing Job: {e}")

async def main():
    stop_event = asyncio.Event()
    task = asyncio.create_task(listener(stop_event))
    await task

if __name__ == '__main__':
    asyncio.run(main())
