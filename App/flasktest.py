from flask import Flask

app = Flask(__name__)

@app.route('/') # type: ignore
def index():
    return "Testing Flask"


app.run(host="0.0.0.0",port=80)