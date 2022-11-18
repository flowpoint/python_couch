from couch.couch import Server, BasicAuth
import pytest

auth = BasicAuth('admin','temppwd')
server = Server("localhost", port=8001, auth=auth)
server.create_db('testdb')


def test_put_doc():
    server.create_db('testdb')
    db = server.get_db('testdb')

    d1 = {"_id":"1", "hello":"world"}
    db.put(d1)
    d2 = db.get('1')
    assert d1 == d2

    server.delete_db('testdb')
