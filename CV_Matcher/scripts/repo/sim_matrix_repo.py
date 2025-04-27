from typing import Optional

import psycopg2
import pandas as pd
from psycopg2 import sql
from psycopg2.extensions import connection


def insert_new_row(conn: connection, new_a_id: int, similarities_df: pd.DataFrame):
    """
    Inserts a new row into the sim_matrix table using a DataFrame.

    :param conn: PostgreSQL database connection object
    :param new_a_id: ID of the new A element
    :param similarities_df: DataFrame with single row containing similarity scores to each B element
    """
    with conn.cursor() as cursor:
        # Get B column names (excluding a_id)
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'sim_matrix' 
            AND column_name != 'id'
            ORDER BY ordinal_position;
        """)
        b_columns = [row[0] for row in cursor.fetchall()]
        b_columns.sort()

        if similarities_df is None:
            cursor.execute(
                'INSERT INTO sim_matrix ("id") VALUES (%s)',
                (new_a_id,)
            )
            conn.commit()
            return

        # Validate DataFrame structure
        if len(similarities_df) != 1:
            raise ValueError("DataFrame must contain exactly one row")

        if len(list(similarities_df.columns)) != len(list(map(int,b_columns))):
            print(list(similarities_df.columns))
            print(list(map(int,b_columns)))
            raise ValueError(f"DataFrame columns must match B columns in order: {b_columns}")

        # Prepare values
        values = [new_a_id] + similarities_df.iloc[0].tolist()
        columns_str = ', '.join(['\"id\"'] + list(map(lambda x: '\"' + x + '\"', b_columns)))
        placeholders = ', '.join(['%s'] * (len(b_columns) + 1))

        # Create and execute INSERT query
        insert_query = f"""
            INSERT INTO sim_matrix ({columns_str})
            VALUES ({placeholders})
        """
        cursor.execute(insert_query, values)
    conn.commit()


def insert_new_column(conn: connection, new_b_id: str, similarities_df: Optional[pd.DataFrame] = None):
    """
    Inserts a new column into the sim_matrix table.
    If similarities_df is given, updates each row; otherwise, only adds the column.

    :param conn: PostgreSQL database connection object
    :param new_b_id: Name/ID of the new B element (column name)
    :param similarities_df: Optional DataFrame with a single column containing similarity scores
    """
    with conn.cursor() as cursor:
        # Add new column if it doesn't exist
        cursor.execute(
            sql.SQL("ALTER TABLE sim_matrix ADD COLUMN IF NOT EXISTS {} DOUBLE PRECISION").format(
                sql.Identifier(new_b_id)
            )
        )

        # Only update values if a DataFrame is provided
        if similarities_df is not None:
            # Get existing element IDs ordered by id
            cursor.execute("SELECT id FROM sim_matrix ORDER BY id;")
            ids = [row[0] for row in cursor.fetchall()]

            # Validate DataFrame structure
            if similarities_df.shape[1] != 1:
                raise ValueError("DataFrame must contain exactly one column")

            if similarities_df.shape[0] != len(ids):
                raise ValueError(f"Need {len(ids)} similarity scores, got {len(similarities_df)}")

            similarities = similarities_df.iloc[:, 0].tolist()

            # Prepare the update statement
            update_query = sql.SQL("""
                UPDATE sim_matrix
                SET {} = %s
                WHERE id = %s
            """).format(sql.Identifier(new_b_id))

            # Update each row
            for id_val, similarity in zip(ids, similarities):
                cursor.execute(update_query, (similarity, id_val))

    # Commit changes after all operations
    conn.commit()