from flask import Flask
import xmltodict
import requests
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    payload = {"date_req1": "01/07/2001", "date_req2": "13/07/2001"}
    r = requests.get("http://www.cbr.ru/scripts/xml_metall.asp", params=payload)
    return str(xmltodict.parse(r.text))
