from sqlfkpath import Key, ForeignKey


def test_key_simple() -> None:
    key=Key(database=None, table="table", columns=["column"])
    assert str(key) == "table(column)"


def test_key_with_database() -> None:
    key=Key(database="database", table="table", columns=["column"])
    assert str(key) == "database.table(column)"


def test_key_multiple_columns() -> None:
    key=Key(database="plugh", table="foo", columns=["bar", "baz", "qux"])
    assert str(key) == "plugh.foo(bar, baz, qux)"


def test_foreign_key() -> None:
    foreign_key = ForeignKey(
        source=Key(database="src_database", table="src_table", columns=["src_column"]),
        destination=Key(database="dst_database", table="dst_table", columns=["dst_column"]),
    )
    assert str(foreign_key) == f"{foreign_key.source} -> {foreign_key.destination}"
