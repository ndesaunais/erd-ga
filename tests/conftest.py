import pathlib
from typing import Any, Generator

import pytest
import sqlalchemy
from sqlalchemy import text
from testcontainers.postgres import PostgresContainer


@pytest.fixture
def postgres_db() -> Generator[str, Any, Any]:
    user = "user"
    password = "passwd"
    db_name = "database"

    with PostgresContainer(
        "postgres:9.5",
        user=user,
        password=password,
        dbname=db_name,
    ) as connection:
        url = connection.get_connection_url()
        engine = sqlalchemy.create_engine(url)
        with engine.connect() as connection:
            yield url, connection


@pytest.fixture
def sql_path():
    return pathlib.Path(__file__).absolute().parent / "sql"


def postgres_with_schema(postgres_db, sql_path, filename):
    url, connection = postgres_db
    with open(sql_path / filename) as file:
        query = text(file.read())
        connection.execute(query)
        connection.commit()
    yield url


@pytest.fixture
def postgres_airbnb(postgres_db, sql_path):
    yield next(postgres_with_schema(postgres_db, sql_path, "airbnb.sql"))


@pytest.fixture
def postgres_analytics(postgres_db, sql_path):
    yield next(postgres_with_schema(postgres_db, sql_path, "analytics.sql"))


@pytest.fixture
def postgres_mflix(postgres_db, sql_path):
    yield next(postgres_with_schema(postgres_db, sql_path, "mflix.sql"))


@pytest.fixture
def postgres_simple(postgres_db, sql_path):
    yield next(postgres_with_schema(postgres_db, sql_path, "simple.sql"))
