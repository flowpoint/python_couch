from couch.couch import Server, BasicAuth
import pytest

def test_server():
    auth = BasicAuth('admin','temppwd')
    server = Server("localhost", port=8001, auth=auth)
    response = server.create_db('testdb')
    db = server.get_db('testdb')
    res = db.put({"_id":"1", "hello":"world"})
    print(f"put {res}")
    '''
    res = db.get("1")
    print(f"get {res}")
    '''
