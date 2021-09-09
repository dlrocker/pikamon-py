import os

"""
Constants or utility functions for testing the SQLite database
"""

TEST_DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
TEST_DB = "test.db"

DEFAULT_RECORDS = [
    ('USER1', 20210101, 20210101),
    ('USER2', 20210102, 20210102),
    ('USER3', 20210103, 20210103)
]


def create_sample_user_records(conn, records=DEFAULT_RECORDS):
    """Helper function to create sample 'user' table records"""
    cursor = conn.cursor()
    cursor.executemany('''INSERT INTO users(user_id, create_date, last_action_date) VALUES (?, ?, ?)''', records)
    conn.commit()
