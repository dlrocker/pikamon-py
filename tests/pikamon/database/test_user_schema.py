import pytest
import sqlite3


def test_user_insert_valid_record(sqlite_conn):
    """Test validating we can insert valid records into our 'users' table"""
    cursor = sqlite_conn.cursor()

    input_tuple = ('USER1', 20210101, 20210101)
    cursor.execute('''INSERT INTO users(user_id, create_date, last_action_date) VALUES (?, ?, ?)''', input_tuple)
    sqlite_conn.commit()

    cursor.execute('''SELECT * from users''')
    result = cursor.fetchall()
    assert len(result) == 1
    assert input_tuple == result[0]


def test_user_insert_many_valid_records(sqlite_conn):
    """Test validating we can insert many valid records into our 'users' table"""
    cursor = sqlite_conn.cursor()

    input_records = [
        ('USER1', 20210101, 20210101),
        ('USER2', 20210102, 20210102),
        ('USER3', 20210103, 20210103)
    ]
    cursor.executemany('''INSERT INTO users(user_id, create_date, last_action_date) VALUES (?, ?, ?)''', input_records)
    sqlite_conn.commit()

    cursor.execute('''SELECT * from users order by user_id asc''')
    result = cursor.fetchall()
    assert input_records == result


def test_user_insert_no_userid(sqlite_conn):
    """
    Test that we cannot insert invalid records into the 'users' table. This test is validating our 'users' schema
    """
    cursor = sqlite_conn.cursor()

    # Validate values cannot be null
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            '''INSERT INTO users(user_id, create_date, last_action_date) VALUES (?, ?, ?)''',
            (None, 20210101, 20210101)
        )
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            '''INSERT INTO users(user_id, create_date, last_action_date) VALUES (?, ?, ?)''',
            ('USER1', None, 20210101)
        )
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            '''INSERT INTO users(user_id, create_date, last_action_date) VALUES (?, ?, ?)''',
            ('USER1', 20210101, None)
        )

    # Validate primary key must be unique
    cursor.execute(
        '''INSERT INTO users(user_id, create_date, last_action_date) VALUES (?, ?, ?)''',
        ('USER1', 20210101, 20210101)
    )
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            '''INSERT INTO users(user_id, create_date, last_action_date) VALUES (?, ?, ?)''',
            ('USER1', 20210102, 20210102)
        )

    # Validate that we can't submit strings for integer values
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            '''INSERT INTO users(user_id, create_date, last_action_date) VALUES (?, ?, ?)''',
            ('USER1', 'USER1', 20210102)
        )
