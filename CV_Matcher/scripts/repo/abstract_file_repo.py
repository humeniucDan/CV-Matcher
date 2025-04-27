import pandas as pd
import psycopg2
import numpy as np
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

from scripts.util.df_util import convert_wide_to_compact, convert_compact_to_wide

DB_CONFIG = {
    "dbname": "CV_Matcher",
    "user": "postgres",
    "password": "omega1234",
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# Save Job embeddings from DataFrame
def save_embeddings(df_orig: pd.DataFrame, collection_name: str) -> pd.DataFrame:
    df = convert_wide_to_compact(df_orig)
    with get_connection() as conn:
        with conn.cursor() as cur:
            ids = []
            # Prepare a reusable SQL template with dynamic table name
            insert_stmt = sql.SQL(
                "INSERT INTO {table} (embedding) VALUES (%s) RETURNING id"
            ).format(
                table=sql.Identifier(collection_name)
            )

            for embedding in df['embedding']:
                # Execute the statement with the current embedding
                cur.execute(insert_stmt, (embedding.tolist(),))
                ids.append(cur.fetchone()[0])

            conn.commit()

    df['id'] = ids
    return df

# Get all Job embeddings as DataFrame
def get_df(collection_name: str) -> pd.DataFrame:
    with get_connection() as conn:
        # Build safe SQL query with dynamic table name
        query = sql.SQL("SELECT * FROM {table} order by id asc").format(
            table=sql.Identifier(collection_name)
        )
        # Convert SQL object to string for pandas
        df = pd.read_sql(query.as_string(conn), conn)

    # Convert stored lists back to numpy arrays
    df['embedding'] = df['embedding'].apply(np.array)
    return convert_compact_to_wide(df)