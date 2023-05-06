import sqlalchemy
from sqlfkpath import Key, ForeignKey, find_paths
from sqlfkpath import reflect, list_foreign_keys, create_table_foreign_key_map

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
    foreign_keys = list(list_foreign_keys(reflect(engine)))
    table_fk_map = create_table_foreign_key_map(foreign_keys)
    found_paths = []
    find_paths(table_fk_map, "child", "parent", [], [], found_paths)
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
