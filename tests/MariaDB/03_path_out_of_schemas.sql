DROP DATABASE IF EXISTS test_03_out;
DROP DATABASE IF EXISTS test_03_in;

CREATE DATABASE test_03_in;
CREATE DATABASE test_03_out;

GRANT ALL PRIVILEGES ON test_03_in.* TO test;
GRANT ALL PRIVILEGES ON test_03_out.* TO test;

USE test_03_in;

CREATE TABLE foo (
    id INT PRIMARY KEY
);

CREATE TABLE bar (
    id INT PRIMARY KEY
);

USE test_03_out;

CREATE TABLE plugh (
    id INT PRIMARY KEY,
    foo_id INT,
    bar_id INT,
    FOREIGN KEY(foo_id) REFERENCES test_03_in.foo(id),
    FOREIGN KEY(bar_id) REFERENCES test_03_in.bar(id)
);
