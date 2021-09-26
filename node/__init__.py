import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import time
import threading
import requests
from block import Block
from agg_qc import AggQC
import json
from qc import QC
from dataclasses import asdict
load_dotenv()


def retry_blocktransfer(i, ports, block):
    while True:
        try:
            url = f"http://node-{i}:{ports[i]}/receive_block"
            response = requests.post(
                url, json=block.as_dict())
            return response
        except:
            continue


def generate_block():
    qc_set = []
    qc = QC(
        "qc", 1, '1dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e0000000000000000', '00000000000000001dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e')
    qc_set.append(qc)
    agg_qc = AggQC(
        qc_set, '00000000000000001dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e')
    block = Block("block", agg_qc, qc, 'abchduehoshdiohsodhoihsd')
    return block


def start_blockgenration():
    print(os.environ['PRIMARY'], flush=True)
    if os.environ['PRIMARY'] == 'True':
        print("I started Block generation", flush=True)
        block = generate_block()
        ports = os.environ['PORTS'].split(',')
        for i in range(0, len(ports)):
            if ports[i] != os.environ['FLASK_RUN_PORT']:
                response = retry_blocktransfer(i, ports, block)
                print(response.content, flush=True)
    else:
        print("I am ready to get the block", flush=True)


def create_app(test_config=None):
    _nodes = os.environ["PUBLIC_KEYS"].split(",")
    _private_key = os.environ["PRIVATE_KEY"]
    node = Flask(__name__, instance_relative_config=True)
    node.config.from_mapping(
        SECRET_KEY=os.environ["SECRET_KEY"],
        DATABASE=os.environ["NODE_ID"] +
        os.environ['FLASK_RUN_PORT'] + ".sqlite"
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        node.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        node.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(node.instance_path)
    except OSError:
        pass

    # If primary then start block generation
    print("Sucessfully started block Initialized", flush=True)
    t1 = threading.Thread(target=start_blockgenration)

    t1.start()
    t1.join()

    print("Sucessfully started block generation", flush=True)

    @ node.route('/')
    def index():
        return 'Healthcheck'

    @ node.route('/status')
    def status():
        return {
            "host": request.remote_addr,
            "port":  os.environ['FLASK_RUN_PORT'],
            "node_id": os.environ["NODE_ID"],
            "private_key": _private_key,
            "public_keys": _nodes,
            "primary":  os.environ["PRIMARY"]
        }

    @ node.route('/receive_block', methods=['POST'])
    def recieve_block():
        return (jsonify(request.json))

    return node
