Create a docker network for this project if it doesn't exist yet:

    docker network create sql-fk-path

Change permissions for setup files, so that the PostgreSQL server user can read
them (may not be necessary depending on the `umask` value on your docker host):

    chmod o+rx tests/PostgreSQL
    chmod o+r tests/PostgreSQL/*.sql

Start the test PostgreSQL server with:

    docker run \
        --rm \
        --name sql-fk-path-postgres \
        --network sql-fk-path \
        --publish 15432:5432 \
        --env POSTGRES_PASSWORD=secret \
        --volume "$PWD/tests/PostgreSQL:/docker-entrypoint-initdb.d" \
        postgres:16.2

Run some tests:

    ./sqlfkpath.py postgresql://postgres:secret@127.0.0.1:15432/postgres test_01_c.child test_01_a.grandparent

    ./sqlfkpath.py postgresql://postgres:secret@127.0.0.1:15432/postgres test_01_a.grandparent test_01_c.child

    ./sqlfkpath.py postgresql://postgres:secret@127.0.0.1:15432/postgres child grandparent

    ./sqlfkpath.py postgresql://postgres:secret@127.0.0.1:15432/postgres grandparent child

    ./sqlfkpath.py postgresql://postgres:secret@127.0.0.1:15432/postgres foo bar
