import os

from flask import Flask, jsonify, redirect

app = Flask(__name__)

SERVER_ID = os.getenv('SERVER_ID', 'default_id')


@app.route('/')
def hello_world():
    return redirect('/home')


@app.route('/home', methods=['GET'])
def home():
    return jsonify(message=f"Hello from Server: {SERVER_ID}", status="successful"), 200


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return 'OK', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
