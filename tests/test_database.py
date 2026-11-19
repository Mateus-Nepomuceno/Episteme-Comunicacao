import pytest

from comunicacao.database import (
    criar_engine,
    normalizar_database_url,
    validar_schema,
)


def test_normalizar_database_url():
    assert (
        normalizar_database_url('postgres://user:pass@host:5432/db')
        == 'postgresql+psycopg://user:pass@host:5432/db'
    )
    assert (
        normalizar_database_url('postgresql://user:pass@host:5432/db')
        == 'postgresql+psycopg://user:pass@host:5432/db'
    )
    assert (
        normalizar_database_url('sqlite:///database.db')
        == 'sqlite:///database.db'
    )


def test_validar_schema():
    assert validar_schema('comunicacao') == 'comunicacao'
    with pytest.raises(ValueError, match='Schema inválido'):
        validar_schema('comunicacao!')


def test_criar_engine_postgres_com_schema():
    pg_engine = criar_engine(
        'postgresql://user:pass@localhost:5432/db', 'comunicacao'
    )
    assert pg_engine.dialect.name == 'postgresql'
    assert pg_engine.pool._pre_ping is True
    pg_engine.dispose()
