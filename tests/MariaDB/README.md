Create a docker network for this project if it doesn't exist yet:

    docker network create sql-fk-path

Change permissions for setup files, so that the MariaDB server user can read
them (may not be necessary depending on the `umask` value on your docker host):

    chmod o+rx tests/MariaDB
    chmod o+r tests/MariaDB/*.sql

Start the test MariaDB server with:

    docker run \
        --rm \
        --name sql-fk-path-mariadb \
        --network sql-fk-path \
        --publish 13306:3306 \
        --env MARIADB_ROOT_PASSWORD=secret \
        --volume "$PWD/tests/MariaDB:/docker-entrypoint-initdb.d" \
        mariadb:11.3

Run some tests:

    ./sqlfkpath.py mysql://test:secret@127.0.0.1:13306/test_01_c child test_01_a.grandparent

    ./sqlfkpath.py mysql://test:secret@127.0.0.1:13306/test_01_c test_01_a.grandparent child

    ./sqlfkpath.py mysql://test:secret@127.0.0.1:13306/test_01_a test_01_c.child grandparent

    ./sqlfkpath.py mysql://test:secret@127.0.0.1:13306/test_01_a grandparent test_01_c.child

    ./sqlfkpath.py mysql://test:secret@127.0.0.1:13306/test_02 child grandparent

    ./sqlfkpath.py mysql://test:secret@127.0.0.1:13306/test_02 grandparent child

    ./sqlfkpath.py mysql://test:secret@127.0.0.1:13306/test_03_in foo bar
