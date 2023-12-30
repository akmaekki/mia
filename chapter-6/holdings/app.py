import socket
import logging

from flask import Flask, jsonify

from holdings import queries

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/ping', methods=["GET"])
def ping():
    return socket.gethostname()


@app.route('/holdings', methods=["GET"])
def holdings():
    logger.debug("akmaekki: requesting /holdings")
    query = queries.Holdings()

    return jsonify(query.all())


if __name__ == "__main__":
    app.run(host='0.0.0.0')
