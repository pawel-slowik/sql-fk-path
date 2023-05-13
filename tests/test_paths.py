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


def db_from_sql(sql: str) -> sqlalchemy.engine.Engine:
    engine = sqlalchemy.create_engine("sqlite://")
    for statement in sql.split(";"):
        engine.execute(statement)
    return engine
