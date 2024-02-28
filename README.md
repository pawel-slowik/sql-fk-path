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

## TODO

- add support for cross-database foreign keys
- refactor the `find_paths` and `gather_paths` functions to use an elegant graph
  traversal algorithm
- handle nonexistent table names in arguments
- use a separate exit code for errors
