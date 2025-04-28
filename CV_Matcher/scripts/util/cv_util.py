import glob

from docx import Document
from fontTools.misc.cython import returns
from google import genai
from google.genai import types
import seaborn as sns
import matplotlib.pyplot as plt

from scripts.util.json_parser import summary_cv
from scripts.util.vector_embedding_util import embed_json, calc_sim_measure

import pandas as pd

def process_cv(cv, df_job_embeddings, id):
    # convert cv docx to json
    cv_json = summary_cv(cv)
    # create vector embedding for cv
    df_cv_embedding = embed_json(cv_json, id)
    # calculate sim measure
    new_sims = calc_sim_measure(df_cv_embedding, df_job_embeddings)
    # return cv_vector_embedding, sim_measure
    return df_cv_embedding, new_sims, cv_json



if __name__ == '__main__': # for test
    def extract_text_from_docx(file_path):
        doc = Document(file_path)
        text = []

        # Extract paragraphs
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)

        # Extract text from tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        text.append(paragraph.text)

        return '\n'.join(text)

    def read_folder(folder_path):
        folder_path = f'{folder_path}/*.docx'

        # Extract text from all .docx files in the folder
        text_array = []
        ids_array = []
        cur_id = 1
        for file_path in glob.glob(folder_path):
            text = extract_text_from_docx(file_path)
            text_array.append(text)
            ids_array.append(cur_id)
            cur_id += 1

        return ids_array, text_array


    cv = """
    Andrei Mihailescu
Technical Skills
- JavaScript, ReactJS, Node.js, SQL
- HTML, CSS, Bootstrap, AngularJS
- Python, Django, PostgreSQL, REST APIs
- TypeScript, VueJS, AWS, Docker
- Java, Spring Boot, OracleSQL, Kubernetes
Foreign Languages
- English: C1
- Spanish: B1
- French: A2
Education
- University Name: Politehnica University of Bucharest
- Program Duration: 4 years
- Master Degree Name: Politehnica University of Bucharest
- Program Duration: 2 years
Certifications
- AWS Certified Solutions Architect – Associate
- Certified Kubernetes Administrator (CKA)
- Oracle Certified Professional, Java SE 11 Developer
Project Experience
1. **Inventory Management System**
   Developed a robust inventory management system using Java and Spring Boot for the backend, with an OracleSQL database to handle complex queries and data storage. Implemented REST APIs to facilitate seamless communication between the backend and a responsive frontend built with AngularJS and Bootstrap. Deployed the application on a Kubernetes cluster, ensuring scalability and high availability. Technologies and tools used: Java, Spring Boot, OracleSQL, AngularJS, Bootstrap, Kubernetes.

2. **Real-time Data Analytics Platform**
   Created a real-time data analytics platform leveraging Python and Django for the backend, with PostgreSQL as the database to manage large datasets efficiently. Utilized ReactJS and TypeScript to build a dynamic and interactive user interface. Integrated AWS services for cloud storage and Docker for containerization, enabling smooth deployment and scalability. Technologies and tools used: Python, Django, PostgreSQL, ReactJS, TypeScript, AWS, Docker.

    """
    GOOGLE_API_KEY = ''
    client = genai.Client(api_key=GOOGLE_API_KEY)
    job_ids, job_texts = read_folder('../../DataSet/job_descriptions')

    number_of_entries = 5
    job_ids = job_ids[:number_of_entries]
    job_texts = job_texts[:number_of_entries]

    job_embeddings = client.models.embed_content(
        model='models/text-embedding-004',
        contents=job_texts,
        config=types.EmbedContentConfig(task_type='semantic_similarity'))

    df_job = pd.DataFrame([e.values for e in job_embeddings.embeddings], index=['job_' + str(cur_id) for cur_id in job_ids])
    embedding, sim = process_cv(cv, df_job)

    mini = sim.min().min()
    maxi = sim.max().max()

    plt.figure(figsize=(10, 8))
    sns.heatmap(sim, vmin=mini, vmax=maxi, cmap='Greens')
    plt.savefig('heatmap_plot.png')
