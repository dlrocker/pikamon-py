import pytest
import sqlite3

from database_helpers import create_sample_user_records  # noqa


def test_pokemon_insert_valid_record_no_users(sqlite_conn):
    """Validate that we fail to insert a valid record into the 'pokemons' table when there is no corresponding
    user in the 'users' table"""
    cursor = sqlite_conn.cursor()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            '''INSERT INTO pokemon(trainer_id, pokemon_number, pokemon_name, pokemon_level) VALUES (?, ?, ?, ?)''',
            ("USER1", 1, "bulbasaur", 1)
        )


def test_pokemon_insert_valid_records(sqlite_conn):
    """Test validating we can insert valid records into our 'users' table"""
    cursor = sqlite_conn.cursor()

    # Create records in the 'users' table
    create_sample_user_records(sqlite_conn)

    input_records = [
        ("USER1", 1, "bulbasaur", 1),
        ("USER1", 2, "ivysaur", 1),
        ("USER2", 1, "bulbasaur", 1),
        ("USER3", 2, "ivysaur", 1)
    ]
    cursor.executemany(
        '''INSERT INTO pokemon(trainer_id, pokemon_number, pokemon_name, pokemon_level) VALUES (?, ?, ?, ?)''',
        input_records
    )
    sqlite_conn.commit()

    cursor.execute('''SELECT trainer_id, pokemon_number, pokemon_name, pokemon_level from pokemon''')
    result = cursor.fetchall()
    assert input_records == result


def test_pokemon_when_we_delete_users(sqlite_conn):
    """Validate that if we delete a user from the 'users' table that corresponding records
    are removed from the 'pokemon' table"""
    cursor = sqlite_conn.cursor()

    # Create records in the 'users' table
    create_sample_user_records(sqlite_conn)

    input_records = [
        ("USER1", 1, "bulbasaur", 1),
        ("USER1", 2, "ivysaur", 1),
        ("USER2", 1, "bulbasaur", 1),
        ("USER3", 2, "ivysaur", 1)
    ]
    cursor.executemany(
        '''INSERT INTO pokemon(trainer_id, pokemon_number, pokemon_name, pokemon_level) VALUES (?, ?, ?, ?)''',
        input_records
    )

    cursor.execute("DELETE FROM users WHERE user_id='USER1';")
    sqlite_conn.commit()

    cursor.execute('''SELECT trainer_id, pokemon_number, pokemon_name, pokemon_level from pokemon''')
    result = cursor.fetchall()
    assert input_records[2:] == result
