from sqlfkpath import Key, ForeignKey


def test_key_simple() -> None:
    key=Key(table="table", columns=["column"])
    assert str(key) == "table(column)"


def test_key_multiple_columns() -> None:
    key=Key(table="foo", columns=["bar", "baz", "qux"])
    assert str(key) == "foo(bar, baz, qux)"


def test_foreign_key() -> None:
    foreign_key = ForeignKey(
        source=Key(table="src_table", columns=["src_column"]),
        destination=Key(table="dst_table", columns=["dst_column"]),
    )
    assert str(foreign_key) == f"{foreign_key.source} -> {foreign_key.destination}"
