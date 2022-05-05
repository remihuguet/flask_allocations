import abc
import os
import sqlite3
from allocation import repository


class AbstractUnitOfWork(abc.ABC):
    products: repository.Repository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def rollback(self):
        pass


class InMemoryUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.products = repository.InMemoryRepository(products=[])
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass


class SQLiteUnitOfWork(AbstractUnitOfWork):
    def __init__(self, connection_factory):
        self.connection_factory = connection_factory

    def __enter__(self):
        self.connection: sqlite3.Connection = self.connection_factory()
        self.products = repository.SQLiteRepository(self.connection)
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()


def sqlite_connection(db_filename: str):
    def _():
        return sqlite3.connect(db_filename)

    return _


def initialize_uow(repo_class):
    if repo_class == "InMemoryRepository":
        return InMemoryUnitOfWork()
    elif repo_class == "SQLiteRepository":
        return SQLiteUnitOfWork(
            connection_factory=sqlite_connection(os.environ.get("SQLITE_DB_FILENAME"))
        )
