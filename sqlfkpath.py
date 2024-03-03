#!/usr/bin/env python3

from __future__ import annotations
import sys
import argparse
import textwrap
from typing import Optional, Iterable, Sequence, Mapping, MutableMapping, NamedTuple, List
import sqlalchemy


class Key(NamedTuple):
    database: Optional[str]
    table: str
    columns: Sequence[str]

    def size_matches(self, other: Key) -> bool:
        return len(self.columns) == len(other.columns)

    def database_type_matches(self, other: Key) -> bool:
        if self.database is None and other.database is None:
            return True
        if self.database is not None and other.database is not None:
            return True
        return False

    def get_fully_qualified_table(self) -> str:
        return self.table if self.database is None else f"{self.database}.{self.table}"

    def list_fully_qualified_columns(self) -> Iterable[str]:
        return [f"{self.get_fully_qualified_table()}.{column}" for column in self.columns]

    def __str__(self) -> str:
        return self.get_fully_qualified_table() + "(" + ", ".join(self.columns) + ")"


class ForeignKey(NamedTuple):
    source: Key
    destination: Key

    @classmethod
    def build(cls, source: Key, destination: Key) -> ForeignKey:
        if not source.size_matches(destination):
            raise ValueError
        if not source.database_type_matches(destination):
            raise ValueError
        return cls(source, destination)

    def join(self) -> str:
        conditions = [
            f"{source_column} = {destination_column}"
            for source_column, destination_column in zip(
                self.source.list_fully_qualified_columns(),
                self.destination.list_fully_qualified_columns(),
            )
        ]
        return f"JOIN {self.destination.get_fully_qualified_table()} ON " + " AND ".join(conditions)

    def __str__(self) -> str:
        return f"{self.source} -> {self.destination}"


class Path:

    def __init__(self, edges: Iterable[ForeignKey]):
        edges = tuple(edges)
        database_types = {type(edge.source.database) for edge in edges}
        if len(database_types) != 1:
            raise ValueError
        self.edges = edges

    def joins(self) -> str:
        return "\n".join(
            [self.edges[0].source.get_fully_qualified_table()]
            + [edge.join() for edge in self.edges]
        )

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

    def get_schema(table_name: str, meta: sqlalchemy.MetaData) -> Optional[str]:
        table_schema: Optional[str] = meta.tables[table_name].schema
        default_schema: Optional[str] = meta.schema
        return table_schema if table_schema is not None else default_schema

    for table in meta.tables.values():
        for constraint in table.constraints:
            if not isinstance(constraint, sqlalchemy.ForeignKeyConstraint):
                continue
            yield ForeignKey.build(
                source=Key(
                    get_schema(table.name, meta),
                    table.name,
                    constraint.column_keys,
                ),
                destination=Key(
                    get_schema(constraint.referred_table.name, meta),
                    constraint.referred_table.name,
                    [element.column.name for element in constraint.elements],
                ),
            )


def create_table_foreign_key_map(
    foreign_keys: Iterable[ForeignKey]
) -> Mapping[str, Iterable[ForeignKey]]:
    table_fk_map: MutableMapping[str, List[ForeignKey]] = {}
    for foreign_key in foreign_keys:
        table = foreign_key.source.get_fully_qualified_table()
        if table not in table_fk_map:
            table_fk_map[table] = []
        table_fk_map[table].append(foreign_key)
        table = foreign_key.destination.get_fully_qualified_table()
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
            foreign_key.destination.get_fully_qualified_table(),
            end_table,
            walked_tables + [current_table],
            walked_keys + [foreign_key],
            found_paths,
        )
        gather_paths(
            table_fk_map,
            foreign_key.source.get_fully_qualified_table(),
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
    found_paths: List[Path] = []
    gather_paths(table_fk_map, begin, end, [], [], found_paths)
    if found_paths:
        minimum_length = min(path.length() for path in found_paths)
        found_paths = list(filter(lambda path: path.length() == minimum_length, found_paths))
    return found_paths


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Use foreign keys to find shortest join paths between two tables in a SQL database."
        )
    )
    parser.add_argument("url", help="database URL")
    parser.add_argument("begin", help="begin with this table")
    parser.add_argument("end", help="end with this table")
    parser.add_argument("-j", "--join", action="store_true", help="print paths as SQL joins")
    args = parser.parse_args()
    found_paths = list(find_paths(sqlalchemy.create_engine(args.url), args.begin, args.end))
    for index, found_path in enumerate(found_paths):
        print(f"path {index + 1}, length {found_path.length()}")
        print(textwrap.indent(found_path.joins() if args.join else str(found_path), "\t"))
    path_exists = len(found_paths) > 0
    return 0 if path_exists else 1


if __name__ == "__main__":
    sys.exit(main())
