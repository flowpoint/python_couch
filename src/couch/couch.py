import requests
import json

class Auth:
    pass

class BasicAuth:
    def __init__(self, user, psw):
        self.user = user
        self.psw = psw

def _auth_to_request_arg(auth):
    if isinstance(auth, BasicAuth):
        return (auth.user, auth.psw)
    else:
        raise RuntimeError()

class Server:
    def __init__(self, host, *args, auth=None, port=5984) :
        self.host = host
        self.port = port
        self.auth = auth

        self._req_auth = _auth_to_request_arg(self.auth)
        self._url = f"http://{self.host}:{self.port}"

    def get_db(self, name):
        db = Database(
                self.host, 
                name, 
                auth=self.auth,
                port=self.port
                )

        return db

    def create_db(self, name):
        url = self._url + f"/{name}"

        response = requests.put(
            url,
            auth=self._req_auth,
            )

        return response.json()

    def delete_db(self, name):
        url = self._url + f"/{name}"

        response = requests.delete(
            url,
            auth=self._req_auth,
            )

        return response.json()




class Database:
    def __init__(self, host, name, *args, auth=None, port=5984):
        self.host = host
        self.port = port
        self.name = name
        self.auth = auth

        self._req_auth = _auth_to_request_arg(self.auth)
        self._url = f"http://{self.host}:{self.port}/{self.name}"


    def get(self, docid, keep_rev=False):
        url = self._url + f"/{docid}"

        response = requests.get(
            url,
            auth=self._req_auth,
            )

        doc = response.json()
        if keep_rev == False:
            doc.pop('_rev')

        return doc
    

    def put(self, 
            doc, 
            overwrite=True,
            ):

        d = doc

        if '_id' in doc: 
            if '_rev' in doc and overwrite == True:
                raise RuntimeError('cant use the _rev key in doc when overwrite is True')

            docid = doc['_id']
            prev_doc = self.get(docid, keep_rev=True)

            if 'error' in prev_doc:
                pass
            else:
                prev_version = prev_doc['_rev']
                d['_rev'] = prev_version


            response = requests.put(
                self._url+f"/{docid}",
                data=json.dumps(d),
                headers={"Content-Type": "application/json"},
                auth=self._req_auth,
                )
        else:
            response = requests.post(
                self._url,
                data=json.dumps(d),
                headers={"Content-Type": "application/json"},
                auth=self._req_auth,
                )

        return response.json()

    def put_design(self, design, doc):
        response = requests.put(
                self._url+f"/_design/{design}",
                data=json.dumps(doc),
                headers={"Content-Type": "application/json"},
                auth=self._req_auth
                )
        return response.json()

    def get_design_view(self, design, view, keys):
        response = requests.get(
                self._url+f"/_design/{design}/_view/{view}",
                headers={"Content-Type": "application/json"},
                auth=self._req_auth
                )
        return response.json()

