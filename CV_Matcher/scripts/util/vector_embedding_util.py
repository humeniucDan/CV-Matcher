from google import genai
from google.genai import types
import pandas as pd

GOOGLE_API_KEY = ''
client = genai.Client(api_key=GOOGLE_API_KEY)

def embed_json(json: str, id: int):
    embedding = client.models.embed_content(
        model='models/text-embedding-004',
        contents=[json],
        config=types.EmbedContentConfig(task_type='semantic_similarity'))

    df_embedding = pd.DataFrame([e.values for e in embedding.embeddings], index=[i for i in range(id, id+1)])
    return df_embedding

def calc_sim_measure(df_cv: pd.DataFrame, df_job: pd.DataFrame):
    if df_cv.shape[1] != df_job.shape[1]:
        return None
    sim = df_cv @ df_job.T
    return sim