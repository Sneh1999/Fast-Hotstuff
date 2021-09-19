from dotenv import load_dotenv
import os
from blspy import (PrivateKey, Util, AugSchemeMPL, PopSchemeMPL,
                   G1Element, G2Element)
from random import randbytes

load_dotenv()

ports = []
public_keys = []
private_keys = []
initial_port = int(os.environ['INITIAL_PORT'])
for i in range(int(os.environ['N'])):
    ports.append(str(initial_port + i))
    seed = randbytes(32)
    sk: PrivateKey = AugSchemeMPL.key_gen(seed)
    pk: G1Element = sk.get_g1()
    sk_bytes: bytes = bytes(sk)  # 32 bytes
    pk_bytes: bytes = bytes(pk)  # 48 bytes
    private_keys.append(sk_bytes.hex()),
    public_keys.append(pk_bytes.hex())

os.system("docker build -t hotstuff-node .")


s = ","
for i in range(int(os.environ['N'])):
    run_cmd = f"docker run -d --expose={ports[i]} -p {ports[i]}:{ports[i]} --env PRIVATE_KEY={private_keys[i]} --env PUBLIC_KEYS={s.join(public_keys)} --env FLASK_RUN_PORT={ports[i]} --env NODE_ID={i} hotstuff-node"
    print(run_cmd)
    os.system(run_cmd)
