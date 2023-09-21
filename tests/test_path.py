from sqlfkpath import Key, ForeignKey, Path


def test_length() -> None:
    path = Path(
        [
            ForeignKey(
                source=Key(table="foo", columns=["bar_id"]),
                destination=Key(table="bar", columns=["id"]),
            ),
            ForeignKey(
                source=Key(table="bar", columns=["qux_id"]),
                destination=Key(table="qux", columns=["id"]),
            ),
        ]
    )
    assert path.length() == 2


def test_equality() -> None:
    path1 = Path(
        [
            ForeignKey(
                source=Key(table="foo", columns=["bar_id"]),
                destination=Key(table="bar", columns=["id"]),
            ),
            ForeignKey(
                source=Key(table="bar", columns=["qux_id"]),
                destination=Key(table="qux", columns=["id"]),
            ),
        ]
    )
    path2 = Path(
        [
            ForeignKey(
                source=Key(table="foo", columns=["bar_id"]),
                destination=Key(table="bar", columns=["id"]),
            ),
            ForeignKey(
                source=Key(table="bar", columns=["qux_id"]),
                destination=Key(table="qux", columns=["id"]),
            ),
        ]
    )
    assert path1 == path2


def test_str() -> None:
    edges = [
        ForeignKey(
            source=Key(table="foo", columns=["bar_id"]),
            destination=Key(table="bar", columns=["id"]),
        ),
        ForeignKey(
            source=Key(table="bar", columns=["qux_id"]),
            destination=Key(table="qux", columns=["id"]),
        ),
    ]
    path = Path(edges)
    assert str(path) == str(edges[0]) + "\n" + str(edges[1])
