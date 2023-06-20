import os
from flask import Flask

EXTERNAL_SERVICE_KEY = os.environ.get('EXTERNAL_SERVICE_KEY')

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
