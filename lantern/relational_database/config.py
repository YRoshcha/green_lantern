import os

DATABASE = {
    "database": "cursor_db",
    "user": "cursor",
    "password": "strong_password",
    "port": 5432,
    "host": "localhost",
}

TEST_DATABASE = {
    "database": "test_cursor_db",
    "user": "test_cursor",
    "password": "strong_password",
    "port": 5432,
    "host": "localhost",
}

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

FIXTURES_PATH = os.path.join(PROJECT_PATH, "fixtures")
