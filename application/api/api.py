from flask import Flask
import time

app = Flask(__name__)

@app.route("/time")
def getTime():
    return {"time": time.time()}