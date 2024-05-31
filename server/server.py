import logging
import os

from flask import Flask, jsonify, redirect

app = Flask(__name__)

SERVER_ID = os.getenv('SERVER_ID', 'default_id')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.basicConfig(
    filename=f'/var/log/server_logs/{SERVER_ID}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


@app.route('/')
def hello_world():
    return redirect('/home')


@app.route('/home', methods=['GET'])
def home():
    logging.info(f"Server ID: {SERVER_ID} received a home request")
    return jsonify(message=f"Hello from Server: {SERVER_ID}", status="successful"), 200


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    logging.info(f"Server ID: {SERVER_ID} received a heartbeat request")
    return 'ISS ALL GOOD', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
