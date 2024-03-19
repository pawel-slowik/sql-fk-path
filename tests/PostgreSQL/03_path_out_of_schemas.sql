DROP SCHEMA IF EXISTS test_03_out CASCADE;

CREATE SCHEMA test_03_out;

CREATE TABLE foo (
    id INT PRIMARY KEY
);

CREATE TABLE bar (
    id INT PRIMARY KEY
);

SET search_path TO test_03_out;

CREATE TABLE plugh (
    id INT PRIMARY KEY,
    foo_id INT,
    bar_id INT,
    FOREIGN KEY(foo_id) REFERENCES public.foo(id),
    FOREIGN KEY(bar_id) REFERENCES public.bar(id)
);
