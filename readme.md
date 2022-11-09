init the couchdb container:
./init_couchdb.sh

create venv:
python -m venv .venv

activate venv:
source .venv/bin/activate

install editable:
pip install -e .

run tests:
pytest -s

package:
pip wheel . -w wheels
