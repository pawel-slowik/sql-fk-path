DROP SCHEMA IF EXISTS test_01_c CASCADE;
DROP SCHEMA IF EXISTS test_01_b CASCADE;
DROP SCHEMA IF EXISTS test_01_a CASCADE;

CREATE SCHEMA test_01_a;
CREATE SCHEMA test_01_b;
CREATE SCHEMA test_01_c;

SET search_path TO test_01_a;

CREATE TABLE grandparent (
    id INT PRIMARY KEY
);

SET search_path TO test_01_b;

CREATE TABLE parent (
    id INT PRIMARY KEY,
    grandparent_id INT,
    FOREIGN KEY(grandparent_id) REFERENCES test_01_a.grandparent(id)
);

SET search_path TO test_01_c;

CREATE TABLE child (
    parent_id INT,
    FOREIGN KEY(parent_id) REFERENCES test_01_b.parent(id)
);
