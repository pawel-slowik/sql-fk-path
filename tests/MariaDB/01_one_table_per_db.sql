DROP DATABASE IF EXISTS test_01_c;
DROP DATABASE IF EXISTS test_01_b;
DROP DATABASE IF EXISTS test_01_a;

CREATE DATABASE test_01_a;
CREATE DATABASE test_01_b;
CREATE DATABASE test_01_c;

GRANT ALL PRIVILEGES ON test_01_a.* TO test;
GRANT ALL PRIVILEGES ON test_01_b.* TO test;
GRANT ALL PRIVILEGES ON test_01_c.* TO test;

USE test_01_a;

CREATE TABLE grandparent (
    id INT PRIMARY KEY
);

USE test_01_b;

CREATE TABLE parent (
    id INT PRIMARY KEY,
    grandparent_id INT,
    FOREIGN KEY(grandparent_id) REFERENCES test_01_a.grandparent(id)
);

USE test_01_c;

CREATE TABLE child (
    parent_id INT,
    FOREIGN KEY(parent_id) REFERENCES test_01_b.parent(id)
);
