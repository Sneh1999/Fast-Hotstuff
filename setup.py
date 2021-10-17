from dotenv import load_dotenv
import os
from blspy import (PrivateKey, Util, AugSchemeMPL, PopSchemeMPL,
                   G1Element, G2Element)
from random import randbytes

load_dotenv()

ports = []
public_keys = []
private_keys = []
initial_port = int(3000)
for i in range(int(5)):
    ports.append(str(initial_port + i))
    seed = randbytes(32)
    sk: PrivateKey = AugSchemeMPL.key_gen(seed)
    pk: G1Element = sk.get_g1()
    sk_bytes: bytes = bytes(sk)  # 32 bytes
    pk_bytes: bytes = bytes(pk)  # 48 bytes
    private_keys.append(sk_bytes.hex()),
    public_keys.append(pk_bytes.hex())


os.system("docker stop $(docker ps -aq)")
os.system("docker rm $(docker ps -aq)")
os.system("docker build -t hotstuff-node .")
os.system("docker network create node-network")

s = ","
primary_index = 0
for i in range(int(5)):
    name = "node-" + str(i)
    if i == 0:
        run_cmd = f"docker run -d --name {name} --net node-network --expose={ports[i]} -p {ports[i]}:{ports[i]} --env PRIVATE_KEY={private_keys[i]} --env PUBLIC_KEYS={s.join(public_keys)} --env FLASK_RUN_PORT={ports[i]} --env PORTS={s.join(ports)}  --env NODE_ID={i} --env PRIMARY=True --env PRIMARY_NODE={primary_index} hotstuff-node "
    else:
        run_cmd = f"docker run -d --name {name} --net node-network --expose={ports[i]} -p {ports[i]}:{ports[i]} --env PRIVATE_KEY={private_keys[i]} --env PUBLIC_KEYS={s.join(public_keys)} --env FLASK_RUN_PORT={ports[i]}  --env PORTS={s.join(ports)} --env NODE_ID={i} --env PRIMARY_NODE={primary_index} --env PRIMARY=False hotstuff-node"
    print(run_cmd)
    os.system(run_cmd)
