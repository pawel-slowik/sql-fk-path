from sqlfkpath import Key, ForeignKey, Path


def test_key_simple() -> None:
    key = ForeignKey(
        source=Key(database=None, table="foo", columns=["bar_id"]),
        destination=Key(database=None, table="bar", columns=["id"]),
    )
    assert key.join() == "JOIN bar ON foo.bar_id = bar.id"


def test_key_with_database() -> None:
    key = ForeignKey(
        source=Key(database="plugh", table="foo", columns=["bar_id"]),
        destination=Key(database="thud", table="bar", columns=["id"]),
    )
    assert key.join() == "JOIN thud.bar ON plugh.foo.bar_id = thud.bar.id"


def test_key_composite() -> None:
    foreign_key = ForeignKey(
        source=Key(database=None, table="src", columns=["col1", "col3", "col2"]),
        destination=Key(database=None, table="dst", columns=["col_a", "col_c", "col_b"]),
    )
    assert foreign_key.join() == (
        "JOIN dst ON "
        "src.col1 = dst.col_a AND src.col3 = dst.col_c AND src.col2 = dst.col_b"
    )


def test_path() -> None:
    path = Path(
        [
            ForeignKey(
                source=Key(database=None, table="child", columns=["parent_id"]),
                destination=Key(database=None, table="parent", columns=["id"]),
            ),
            ForeignKey(
                source=Key(database=None, table="parent", columns=["grandparent_id"]),
                destination=Key(database=None, table="grandparent", columns=["id"]),
            ),
        ]
    )
    assert path.joins() == (
        "child\n"
        "JOIN parent ON child.parent_id = parent.id\n"
        "JOIN grandparent ON parent.grandparent_id = grandparent.id"
    )


def test_path_with_databases() -> None:
    path = Path(
        [
            ForeignKey(
                source=Key(database="db1", table="child", columns=["parent_id"]),
                destination=Key(database="db2", table="parent", columns=["id"]),
            ),
            ForeignKey(
                source=Key(database="db2", table="parent", columns=["grandparent_id"]),
                destination=Key(database="db3", table="grandparent", columns=["id"]),
            ),
        ]
    )
    assert path.joins() == (
        "db1.child\n"
        "JOIN db2.parent ON db1.child.parent_id = db2.parent.id\n"
        "JOIN db3.grandparent ON db2.parent.grandparent_id = db3.grandparent.id"
    )
