import os
import pytest

from pikamon.constants import DATABASE_NAME, DATABASE_CONFIG_PATH_ENV_VAR
from pikamon.database.connect import setup_database


def test_setup_database_invalid_sql_config_path():
    """Test setup function with invalid path to the SQL configuration for our tables"""
    with pytest.raises(FileNotFoundError):
        setup_database(table_sql_path="/fake/path")
    os.remove(DATABASE_NAME)


def test_setup_database_invalid_sql_config_path_as_env_variable():
    """Test setup function with invalid path to the SQL configuration for our tables set as the environment
    variable. We expect it to use whatever the current directory is"""
    os.environ[DATABASE_CONFIG_PATH_ENV_VAR] = "/fake/path"
    setup_database(table_sql_path=None)
    os.remove(DATABASE_NAME)
    assert True
