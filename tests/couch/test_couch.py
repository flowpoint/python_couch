from couch.couch import Server, BasicAuth
import pytest

auth = BasicAuth('testuser','testpsw')
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

def test_simple_view():
    server.create_db('testdb')
    db = server.get_db('testdb')

    d1 = {"_id":"1", "document_type":"sequencer_run"}
    db.put(d1)

    d1 = {"_id":"2", "document_type":"sequencer_run"}
    db.put(d1)

    map_fn = '''
    function (doc) {
      if(doc.document_type == 'sequencer_run')
        emit(doc, 1);
        }
    '''
    response = db.put_design('runs', {'views':{'aview':{"map":map_fn}}})
    response = db.get_design_view('runs', 'aview', None)

    rid = [x['id'] for x in response['rows']]
    did = ["1", "2"]

    assert set(rid) == set(did)
    server.delete_db('testdb')
