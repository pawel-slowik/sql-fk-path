![Build Status][build-badge]

[build-badge]: https://github.com/pawel-slowik/sql-fk-path/workflows/tests/badge.svg

This script searches for paths created by foreign keys between two SQL tables.

## Installation

Clone this repository and make sure you have Python 3.x and
[SQLAlchemy][sqlalchemy] installed:

	pip3 install -r requirements.txt

You will also need to install a [SQLAlchemy dialect][sqlalchemy-dialect]
suitable for your database:

	pip3 install mysqlclient

[sqlalchemy]:https://www.sqlalchemy.org/
[sqlalchemy-dialect]:https://docs.sqlalchemy.org/en/latest/dialects/index.html

With Docker:

	docker-compose build

## Example usage

	~/path/sqlfkpath.py mysql://user:password@host/database begin_table end_table

With Docker:

	docker-compose run --rm cmd ./sqlfkpath.py mysql://user:password@host/database begin_table end_table

The script will exit with code 0 if there's at least one path found and with
code 1 if there are no paths.

## Limitations

- The script will try to discover foreign key constraints in all available
  schemas. This is necessary because a constraint linking two tables could be
  placed in a schema that is separate from the linked tables. Since for
  [MySQL][mysql-database-is-schema] and [MariaDB][mariadb-database-is-schema] a
  schema is synonymous with a database, this means that for these systems the
  script will inspect all databases. There is currently no way to disable that
  behaviour.

[mysql-database-is-schema]:https://dev.mysql.com/doc/refman/8.0/en/create-database.html
[mariadb-database-is-schema]:https://mariadb.com/kb/en/create-database/

## TODO

- refactor the `find_paths` and `gather_paths` functions to use an elegant graph
  traversal algorithm
- handle nonexistent table names in arguments
- use a separate exit code for errors
