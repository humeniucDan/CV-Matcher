import asyncio
import redis.asyncio as redis
import scripts.repo.filebase_repo as filebase
from scripts.repo.cv_repo import save_cv_embeddings, get_cvs_df
from scripts.repo.job_repo import get_jobs_df, save_job_embeddings
from scripts.repo.sim_matrix_repo import insert_new_row, insert_new_column
from scripts.util import cv_util, job_util
from scripts.repo.abstract_file_repo import get_connection

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
        print('CV: ' + data.decode('utf-8'))
        cv = filebase.get_object(file)

        cv_id = int(data.decode('utf-8').split('.')[0])
        # TODO: cache job_vector_embeddings for better performance
        job_vector_embeddings = get_jobs_df()
        cv_embedding, sim_measures, json_cv = cv_util.process_cv(cv, job_vector_embeddings, cv_id)
        # save cv_vector_embedding in db
        save_cv_embeddings(cv_embedding)
        # insert new sim_measure 'row'
        # if sim_measures is not None:
        insert_new_row(get_connection(), cv_id, sim_measures)

        file_insert = f'cv-processed/{cv_id}.json'
        filebase.put_object(file_insert, json_cv)
    except Exception as e:
        print(f"Error processing CV: {e}")

async def process_job(data: bytes):
    try:
        file = f'job-raw/{data.decode('utf-8')}'
        print("Process job:", file)
        print('job: ' + data.decode('utf-8'))
        job = filebase.get_object(file)

        job_id = int(data.decode('utf-8').split('.')[0])
        # TODO: cache cv_vector_embeddings for better performance
        cv_vector_embeddings = get_cvs_df()
        job_embedding, sim_measures, json_job = job_util.process_job(cv_vector_embeddings, job, job_id)
        # save job_vector_embedding in db
        save_job_embeddings(job_embedding)
        # insert new sim_measure 'row'
        insert_new_column(get_connection(), str(job_id), sim_measures)

        file_insert = f'job-processed/{job_id}.json'
        filebase.put_object(file_insert, json_job)

    except Exception as e:
        print(f"Error processing Job: {e}")

async def main():
    stop_event = asyncio.Event()
    task = asyncio.create_task(listener(stop_event))
    await task

if __name__ == '__main__':
    asyncio.run(main())
