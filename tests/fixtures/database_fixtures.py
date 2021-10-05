import pytest
import os

from pikamon.database.connect import setup_database
from database_helpers import TEST_DB_PATH, TEST_DB  # noqa

"""
Reusable pytest fixture(s) for testing our SQLite database
"""


@pytest.fixture(scope="function", autouse=True)
def sqlite_conn():
    """
    A fully setup test database connection complete with our expected tables.
    """
    conn = setup_database(TEST_DB_PATH, TEST_DB)
    yield conn
    conn.close()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
