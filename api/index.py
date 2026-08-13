import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is working!", 200

@app.route('/test')
def test():
    return "Test is working!", 200

if __name__ == "__main__":
    app.run()
