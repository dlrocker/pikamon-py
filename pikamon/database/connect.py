import sqlite3
import os
import logging

from pikamon.constants import SqliteDB

logger = logging.getLogger(__name__)


def create_bot_tables(conn, tables):
    """Create the tables required for our Pikamon bot in SQLite

    Parameters
    ----------
    conn : sqlite3.Connection
        SQLite Connection Object
    tables : list of str
        List of filepaths to SQL definition files of our tables
    """
    cursor = conn.cursor()

    for table in tables:
        logger.info(f"Creating table {table} if it does not exist.")
        with open(table, 'r') as f:
            create_table_sql = "".join(f.readlines())
        cursor.execute(create_table_sql)
    conn.commit()


def create_connection(database_path=None, database=SqliteDB.DATABASE_NAME):
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


def setup_database(database_path=None, db_name=SqliteDB.DATABASE_NAME, table_sql_path=None):
    """Sets up our database connection and creates all necessary tables for our bot in SQLite

    Parameters
    ----------
    database_path : str
        Directory path for where to write out the database to
    db_name : str
        Name of the database to create under the specified path
    table_sql_path : str
        Directory path to where the SQL definition files for our database are stored. This should not include
        the SQL definition file names.

    Returns
    -------
    connection: sqlite3.Connection
        SQLite Connection Object
    """
    conn = create_connection(database_path, db_name)
    if not table_sql_path:
        database_config_path = os.environ.get(SqliteDB.DATABASE_CONFIG_PATH_ENV_VAR)
        if database_config_path and os.path.isdir(database_config_path):
            logger.info("Using environment variable '{}' to define the path to the table SQL definitions".format(
                SqliteDB.DATABASE_CONFIG_PATH_ENV_VAR))
            table_sql_path = os.environ.get(SqliteDB.DATABASE_CONFIG_PATH_ENV_VAR)
        else:
            table_sql_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "..",
                "..",
                "configuration",
                "database"
            )
    logger.debug(
        "Using '{}' as the path to the SQL file definitions of the bot tables in SQLite".format(table_sql_path))
    tables = [
        os.path.join(table_sql_path, "users.sql"),
        os.path.join(table_sql_path, "pokemon.sql")
    ]
    create_bot_tables(conn, tables)
    # Enforce foreign keys
    conn.execute("PRAGMA foreign_keys = 1")
    conn.commit()
    return conn
