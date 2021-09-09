import sqlite3
import os

from pikamon.constants import DATABASE_NAME


def create_bot_tables(conn, tables):
    cursor = conn.cursor()

    for table in tables:
        with open(table, 'r') as f:
            create_table_sql = "".join(f.readlines())
        cursor.execute(create_table_sql)
    conn.commit()


def create_connection(database_path=None, database=DATABASE_NAME):
    """Creates a connection to the SQLite database for the bot

    Parameters
    ----------
    database_path : string
        Fully qualified path URI to where the database contents should be stored.
        This is only the directory path, it is not the name of the database. Default: None.
    database : String
        The name of the database to create. Default: pikamon.constants.DATABASE_NAME

    Returns
    -------
    connection: sqlite3.Connection
        SQLite Connection Object
    """
    if database_path and os.path.isdir(database_path):
        # If provided a directory for the database to be stored that is VALID, create the database there.
        return sqlite3.connect(os.path.join(database_path, database))
    else:
        # If no database path is provided or the database path is not a directory, make the database in
        # the current location
        return sqlite3.connect(database)


def setup_database(database_path=None, db_name=DATABASE_NAME, table_sql_path=None):
    conn = create_connection(database_path, db_name)
    if not table_sql_path:
        table_sql_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "..",
            "configuration",
            "database"
        )
    tables = [
        os.path.join(table_sql_path, "users.sql"),
        os.path.join(table_sql_path, "pokemon.sql")
    ]
    create_bot_tables(conn, tables)
    # Enforce foreign keys
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


if __name__ == "__main__":
    connection = setup_database()
    connection.close()
