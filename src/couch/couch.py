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



class Database:
    def __init__(self, host, name, *args, auth=None, port=5984):
        self.host = host
        self.port = port
        self.name = name
        self.auth = auth

        self._req_auth = _auth_to_request_arg(self.auth)
        self._url = f"http://{self.host}:{self.port}/{self.name}"

    def get(self, docid):
        url = self._url + f"{docid}"

        response = requests.get(
            url,
            auth=self._req_auth,
            )

        return response.json()
    
    def put(self, 
            doc, 
            overwrite=True,
            ):

        docid = doc['_id']
        d = doc
        prev_doc = self.get(docid)

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

        return response.json()
