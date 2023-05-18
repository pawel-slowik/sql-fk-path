import sqlalchemy
from sqlfkpath import Key, ForeignKey, find_paths


def test_key_simple() -> None:
    engine = db_from_sql("""
        CREATE TABLE parent (
            id INT
        );

        CREATE TABLE child (
            parent_id INT,
            FOREIGN KEY(parent_id) REFERENCES parent(id)
        );
    """)
    found_paths = find_paths(engine, "child", "parent")
    expected_path = [
        ForeignKey(
            source=Key(table="child", columns=["parent_id"]),
            destination=Key(table="parent", columns=["id"]),
        ),
    ]
    assert found_paths == [expected_path]


def test_key_reversed() -> None:
    engine = db_from_sql("""
        CREATE TABLE parent (
            id INT
        );

        CREATE TABLE child (
            parent_id INT,
            FOREIGN KEY(parent_id) REFERENCES parent(id)
        );
    """)
    found_paths = find_paths(engine, "parent", "child")
    expected_path = [
        ForeignKey(
            source=Key(table="child", columns=["parent_id"]),
            destination=Key(table="parent", columns=["id"]),
        ),
    ]
    assert found_paths == [expected_path]


def test_two_steps() -> None:
    engine = db_from_sql("""
        CREATE TABLE grandparent (
            id INT
        );

        CREATE TABLE parent (
            id INT,
            grandparent_id INT,
            FOREIGN KEY(grandparent_id) REFERENCES grandparent(id)
        );

        CREATE TABLE child (
            parent_id INT,
            FOREIGN KEY(parent_id) REFERENCES parent(id)
        );
    """)
    found_paths = find_paths(engine, "child", "grandparent")
    expected_paths = [
        [
            ForeignKey(
                source=Key(table="child", columns=["parent_id"]),
                destination=Key(table="parent", columns=["id"]),
            ),
            ForeignKey(
                source=Key(table="parent", columns=["grandparent_id"]),
                destination=Key(table="grandparent", columns=["id"]),
            ),
        ],
    ]
    assert found_paths == expected_paths


def test_alternative_paths() -> None:
    engine = db_from_sql("""
        CREATE TABLE right (
            id INT
        );

        CREATE TABLE left (
            id INT,
            right_id INT,
            FOREIGN KEY(right_id) REFERENCES right(id)
        );

        CREATE TABLE top (
            id INT,
            left_id INT,
            right_id INT,
            FOREIGN KEY(left_id) REFERENCES left(id),
            FOREIGN KEY(right_id) REFERENCES right(id)
        );
    """)
    found_paths = find_paths(engine, "left", "right")
    expected_paths = [
        [
            ForeignKey(
                source=Key(table="top", columns=["left_id"]),
                destination=Key(table="left", columns=["id"]),
            ),
            ForeignKey(
                source=Key(table="top", columns=["right_id"]),
                destination=Key(table="right", columns=["id"]),
            ),
        ],
        [
            ForeignKey(
                source=Key(table="left", columns=["right_id"]),
                destination=Key(table="right", columns=["id"]),
            ),
        ],
    ]
    assert sorted(found_paths) == sorted(expected_paths)


def test_loop() -> None:
    engine = db_from_sql("""
        CREATE TABLE begin (
            id INT,
            middle_id INT,
            FOREIGN KEY(middle_id) REFERENCES middle(id)
        );

        CREATE TABLE middle (
            id INT,
            loop1_id INT,
            end_id INT,
            FOREIGN KEY(loop1_id) REFERENCES loop1(id),
            FOREIGN KEY(end_id) REFERENCES end(id)
        );

        CREATE TABLE loop1 (
            id INT,
            loop2_id INT,
            FOREIGN KEY(loop2_id) REFERENCES loop2(id)
        );

        CREATE TABLE loop2 (
            id INT,
            middle_id INT,
            FOREIGN KEY(middle_id) REFERENCES middle(id)
        );

        CREATE TABLE end (
            id INT
        );
    """)
    found_paths = find_paths(engine, "begin", "end")
    expected_paths = [
        [
            ForeignKey(
                source=Key(table="begin", columns=["middle_id"]),
                destination=Key(table="middle", columns=["id"]),
            ),
            ForeignKey(
                source=Key(table="middle", columns=["end_id"]),
                destination=Key(table="end", columns=["id"]),
            ),
        ],
    ]
    assert found_paths == expected_paths


def test_double() -> None:
    engine = db_from_sql("""
        CREATE TABLE foo (
            id INT,
            bar_id1 INT,
            bar_id2 INT,
            FOREIGN KEY(bar_id1) REFERENCES bar(id1),
            FOREIGN KEY(bar_id2) REFERENCES bar(id2)
        );

        CREATE TABLE bar (
            id1 INT,
            id2 INT
        );
    """)
    found_paths = find_paths(engine, "foo", "bar")
    expected_paths = [
        [
            ForeignKey(
                source=Key(table="foo", columns=["bar_id1"]),
                destination=Key(table="bar", columns=["id1"]),
            ),
        ],
        [
            ForeignKey(
                source=Key(table="foo", columns=["bar_id2"]),
                destination=Key(table="bar", columns=["id2"]),
            ),
        ],
    ]
    assert sorted(found_paths) == sorted(expected_paths)


def test_composite() -> None:
    engine = db_from_sql("""
        CREATE TABLE qux (
            id1 INT,
            id2 INT
        );

        CREATE TABLE baz (
            qux_id1 INT,
            qux_id2 INT,
            FOREIGN KEY(qux_id1, qux_id2) REFERENCES qux(id1, id2)
        );
    """)
    found_paths = find_paths(engine, "qux", "baz")
    expected_paths = [
        [
            ForeignKey(
                source=Key(table="baz", columns=["qux_id1", "qux_id2"]),
                destination=Key(table="qux", columns=["id1", "id2"]),
            ),
        ]
    ]
    assert found_paths == expected_paths


def db_from_sql(sql: str) -> sqlalchemy.engine.Engine:
    engine = sqlalchemy.create_engine("sqlite://")
    for statement in sql.split(";"):
        engine.execute(statement)
    return engine
