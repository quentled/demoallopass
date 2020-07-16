import json
from typing import Dict

import requests
from flask import Flask, render_template

app = Flask(__name__)


def get_result(url: str) -> str:
    try:
        r = requests.get(url)
        if r.status_code == 200:

            return r.text
        else:
            raise Exception()
    except:
        raise


def parse_res(data: str) -> Dict:
    try:
        j: Dict = json.loads(data)
        records = j.get("records", [])
        result = []

        for record in records:
            fields = record.get("fields", {})
            heure = fields.get("bm_heure")
            prevision = fields.get("bm_prevision")
            res_t = (heure, prevision)
            result.append(res_t)
    except:
        raise
    return result
    pass


def main():
    url = "https://opendata.bordeaux-metropole.fr/api/records/1.0/search/?dataset=ci_courb_a&rows=193"
    try:
        data = get_result(url)
    except:
        pass
    else:
        res = parse_res(data)
    return res


@app.route('/')
def hello_world():
    results = main()
    return render_template('prevision.html', results=results)


if __name__ == "__main__":
    app.run()
    pass
