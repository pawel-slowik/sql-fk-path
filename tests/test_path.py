from sqlfkpath import Key, ForeignKey, Path


def test_length() -> None:
    path = Path(
        [
            ForeignKey(
                source=Key(database=None, table="foo", columns=["bar_id"]),
                destination=Key(database=None, table="bar", columns=["id"]),
            ),
            ForeignKey(
                source=Key(database=None, table="bar", columns=["qux_id"]),
                destination=Key(database=None, table="qux", columns=["id"]),
            ),
        ]
    )
    assert path.length() == 2


def test_equality() -> None:
    path1 = Path(
        [
            ForeignKey(
                source=Key(database=None, table="foo", columns=["bar_id"]),
                destination=Key(database=None, table="bar", columns=["id"]),
            ),
            ForeignKey(
                source=Key(database=None, table="bar", columns=["qux_id"]),
                destination=Key(database=None, table="qux", columns=["id"]),
            ),
        ]
    )
    path2 = Path(
        [
            ForeignKey(
                source=Key(database=None, table="foo", columns=["bar_id"]),
                destination=Key(database=None, table="bar", columns=["id"]),
            ),
            ForeignKey(
                source=Key(database=None, table="bar", columns=["qux_id"]),
                destination=Key(database=None, table="qux", columns=["id"]),
            ),
        ]
    )
    assert path1 == path2


def test_equality_with_databases() -> None:
    db_path1 = Path(
        [
            ForeignKey(
                source=Key(database="plugh", table="foo", columns=["bar_id"]),
                destination=Key(database="thud", table="bar", columns=["id"]),
            ),
            ForeignKey(
                source=Key(database="thud", table="bar", columns=["qux_id"]),
                destination=Key(database="thud", table="qux", columns=["id"]),
            ),
        ]
    )
    db_path2 = Path(
        [
            ForeignKey(
                source=Key(database="plugh", table="foo", columns=["bar_id"]),
                destination=Key(database="thud", table="bar", columns=["id"]),
            ),
            ForeignKey(
                source=Key(database="thud", table="bar", columns=["qux_id"]),
                destination=Key(database="thud", table="qux", columns=["id"]),
            ),
        ]
    )
    assert db_path1 == db_path2


def test_str() -> None:
    edges = [
        ForeignKey(
            source=Key(database="thud", table="foo", columns=["bar_id"]),
            destination=Key(database="plugh", table="bar", columns=["id"]),
        ),
        ForeignKey(
            source=Key(database="plugh", table="bar", columns=["qux_id"]),
            destination=Key(database="plugh", table="qux", columns=["id"]),
        ),
    ]
    path = Path(edges)
    assert str(path) == str(edges[0]) + "\n" + str(edges[1])
