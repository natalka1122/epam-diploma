from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    data = [
        {
            "date": "date111",
            "code": "code",
            "m_name": "m_name",
            "bbb": "bbb",
            "sss": "sss",
        },
        {
            "date": "date222",
            "code": "code",
            "m_name": "m_name",
            "bbb": "bbb",
            "sss": "sss",
        },
    ]
    return render_template("main.jinja", name="vasya", data=data)
