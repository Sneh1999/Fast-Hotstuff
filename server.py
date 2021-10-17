import socket
import os
from dotenv import load_dotenv
import time
import threading
from block import Block
from agg_qc import AggQC
import json
from qc import QC
from dataclasses import asdict

load_dotenv()

# Initialize the host and the port
name = "node-" + os.environ['NODE_ID']
host = socket.gethostbyname(name)
port = os.environ['FLASK_RUN_PORT']
# Split the nodes and the private keys
_public_keys = os.environ["PUBLIC_KEYS"].split(",")
_private_key = os.environ["PRIVATE_KEY"]
ports = os.environ['PORTS'].split(',')
# Create a server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, int(port)))
s.listen(len(_public_keys))

if os.environ['PRIMARY'] == 'True':
    for i in range(len(ports)):
        if (i == 0):
            continue

        print("I started Block generation", flush=True)
        c, addr = s.accept()
        print(addr, flush=True)
        print("CONNECTION CREATED", flush=True)
        qc_set = []
        qc = QC(
            "qc", 1, '1dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e0000000000000000', '00000000000000001dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e')
        qc_set.append(qc)
        agg_qc = AggQC(
            qc_set, '00000000000000001dbd981fe6985776b644b173a4d0385ddc1aa2a829688d1e')
        block = Block("block", agg_qc, qc, 'abchduehoshdiohsodhoihsd')
        # if sequence is zero ignore the qc
        if ports[i] != os.environ['FLASK_RUN_PORT']:
            while True:
                try:
                    print(f"Attempting to send message to {ports[i]}")
                    user_encode_data = json.dumps(
                        block.as_dict()).encode('utf-8')
                    c.send(user_encode_data)
                    c.close()
                    break
                except:
                    print(
                        f"Failed to send message to {ports[i]}. Retrying in 1 sec...")
                    time.sleep(1)
                    continue
            print("Block transfer successful", flush=True)
else:
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    primary_host = socket.gethostbyname(f"node-{os.environ['PRIMARY_NODE']}")
    primary_port = int(ports[int(os.environ['PRIMARY_NODE'])])
    while True:
        try:
            client_socket.connect((primary_host, primary_port))
            break
        except:
            time.sleep(1)
            continue

    print("Connected to primary successfully")
    while True:
        msg = client_socket.recv(1024)
        msg_decoded = msg.decode()
        if len(msg_decoded) > 0:
            print(f"Received {msg_decoded}", flush=True)
