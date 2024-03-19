CREATE TABLE grandparent (
    id INT PRIMARY KEY
);

CREATE TABLE parent (
    id INT PRIMARY KEY,
    grandparent_id INT,
    FOREIGN KEY(grandparent_id) REFERENCES grandparent(id)
);

CREATE TABLE child (
    parent_id INT,
    FOREIGN KEY(parent_id) REFERENCES parent(id)
);
