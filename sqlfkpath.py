#!/usr/bin/env python3

from __future__ import annotations
import sys
import argparse
import textwrap
from typing import Iterable, Sequence, Mapping, MutableMapping, NamedTuple, List
import sqlalchemy


class Key(NamedTuple):
    table: str
    columns: Sequence[str]

    def size_matches(self, other: Key) -> bool:
        return len(self.columns) == len(other.columns)

    def __str__(self) -> str:
        return self.table + "(" + ", ".join(self.columns) + ")"


class ForeignKey(NamedTuple):
    source: Key
    destination: Key

    @classmethod
    def build(cls, source: Key, destination: Key) -> ForeignKey:
        if source.size_matches(destination):
            return cls(source, destination)
        raise ValueError

    def __str__(self) -> str:
        return f"{self.source} -> {self.destination}"


class Path:

    def __init__(self, edges: Iterable[ForeignKey]):
        self.edges = tuple(edges)

    def __str__(self) -> str:
        return "\n".join(map(str, self.edges))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Path):
            return NotImplemented
        return self.edges == other.edges

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Path):
            return NotImplemented
        return self.edges < other.edges

    def length(self) -> int:
        return len(self.edges)


def reflect(engine: sqlalchemy.engine.Engine) -> sqlalchemy.MetaData:
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


def create_table_foreign_key_map(
    foreign_keys: Iterable[ForeignKey]
) -> Mapping[str, Iterable[ForeignKey]]:
    table_fk_map: MutableMapping[str, List[ForeignKey]] = {}
    for foreign_key in foreign_keys:
        table = foreign_key.source.table
        if table not in table_fk_map:
            table_fk_map[table] = []
        table_fk_map[table].append(foreign_key)
        table = foreign_key.destination.table
        if table not in table_fk_map:
            table_fk_map[table] = []
        table_fk_map[table].append(foreign_key)
    return table_fk_map


def gather_paths(
    table_fk_map: Mapping[str, Iterable[ForeignKey]],
    current_table: str,
    end_table: str,
    walked_tables: List[str],
    walked_keys: List[ForeignKey],
    found_paths: List[Path],
) -> None:
    if current_table in walked_tables:
        return
    if current_table == end_table:
        found_paths.append(Path(walked_keys))
        return
    for foreign_key in table_fk_map[current_table]:
        gather_paths(
            table_fk_map,
            foreign_key.destination.table,
            end_table,
            walked_tables + [current_table],
            walked_keys + [foreign_key],
            found_paths,
        )
        gather_paths(
            table_fk_map,
            foreign_key.source.table,
            end_table,
            walked_tables + [current_table],
            walked_keys + [foreign_key],
            found_paths,
        )


def find_paths(engine: sqlalchemy.engine.Engine, begin: str, end: str) -> Iterable[Path]:
    meta = reflect(engine)
    foreign_keys = list(list_foreign_keys(meta))
    table_fk_map = create_table_foreign_key_map(foreign_keys)
    # TODO: put the foreign keys in a graph: tables are nodes, foreign keys are edges
    # TODO: traverse the graph to find paths
    # TODO: optimize
    found_paths: List[Path] = []
    gather_paths(table_fk_map, begin, end, [], [], found_paths)
    return found_paths


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Use foreign keys to find join paths between two tables in a SQL database."
    )
    parser.add_argument("url", help="database URL")
    parser.add_argument("begin", help="begin with this table")
    parser.add_argument("end", help="end with this table")
    args = parser.parse_args()
    found_paths = list(find_paths(sqlalchemy.create_engine(args.url), args.begin, args.end))
    for index, found_path in enumerate(found_paths):
        print(f"path {index + 1}, length {found_path.length()}")
        print(textwrap.indent(str(found_path), "\t"))
    path_exists = len(found_paths) > 0
    return 0 if path_exists else 1


if __name__ == "__main__":
    sys.exit(main())
