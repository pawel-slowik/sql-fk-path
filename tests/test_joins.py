from sqlfkpath import Key, ForeignKey, Path


def test_key_simple() -> None:
    key = ForeignKey(
        source=Key(table="foo", columns=["bar_id"]),
        destination=Key(table="bar", columns=["id"]),
    )
    assert key.join() == "JOIN bar ON foo.bar_id = bar.id"


def test_key_composite() -> None:
    foreign_key = ForeignKey(
        source=Key(table="src", columns=["col1", "col3", "col2"]),
        destination=Key(table="dst", columns=["col_a", "col_c", "col_b"]),
    )
    assert foreign_key.join() == (
        "JOIN dst ON "
        "src.col1 = dst.col_a AND src.col3 = dst.col_c AND src.col2 = dst.col_b"
    )


def test_path() -> None:
    path = Path(
        [
            ForeignKey(
                source=Key(table="child", columns=["parent_id"]),
                destination=Key(table="parent", columns=["id"]),
            ),
            ForeignKey(
                source=Key(table="parent", columns=["grandparent_id"]),
                destination=Key(table="grandparent", columns=["id"]),
            ),
        ]
    )
    assert path.joins() == (
        "child\n"
        "JOIN parent ON child.parent_id = parent.id\n"
        "JOIN grandparent ON parent.grandparent_id = grandparent.id"
    )
