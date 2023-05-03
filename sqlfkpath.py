#!/usr/bin/env python3

from __future__ import annotations
import sys
import argparse
from typing import Iterable, Sequence, NamedTuple
import sqlalchemy


class Key(NamedTuple):
    table: str
    columns: Sequence[str]

    def size_matches(self, other: Key) -> bool:
        if len(self.columns) != len(other.columns):
            return False
        if len(set(self.columns)) != len(set(other.columns)):
            return False
        return True


class ForeignKey(NamedTuple):
    source: Key
    destination: Key

    @classmethod
    def build(cls, source: Key, destination: Key) -> ForeignKey:
        if source.size_matches(destination):
            return cls(source, destination)
        raise ValueError


def reflect(db_url: str) -> sqlalchemy.MetaData:
    engine = sqlalchemy.create_engine(db_url)
    meta = sqlalchemy.MetaData()
    meta.reflect(bind=engine)
    return meta


def list_foreign_keys(meta: sqlalchemy.MetaData) -> Iterable[ForeignKey]:
    for table in meta.tables.values():
        for constraint in table.constraints:
            if not isinstance(constraint, sqlalchemy.ForeignKeyConstraint):
                continue
            yield ForeignKey.build(
                source=Key(
                    table.name,
                    constraint.column_keys,
                ),
                destination=Key(
                    constraint.referred_table.name,
                    [element.column.name for element in constraint.elements],
                ),
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Use foreign keys to find join paths between two tables in a SQL database."
    )
    parser.add_argument("url", help="database URL")
    parser.add_argument("begin", help="begin with this table")
    parser.add_argument("end", help="end with this table")
    args = parser.parse_args()
    meta = reflect(args.url)
    test = list(list_foreign_keys(meta))
    # TODO: put the foreign keys in a graph: tables are nodes, foreign keys are edges
    # TODO: traverse the graph to find paths
    # TODO: optimize
    for foreign_key in test:
        print(foreign_key)
    path_exists = len(test) > 0
    return 0 if path_exists else 1


if __name__ == "__main__":
    sys.exit(main())
