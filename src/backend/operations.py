import os
from datetime import datetime
import signature as sign

# Generates key pair with a given password
def generate_keys(password : bytearray):
    priv = sign.generate_private_key()
    pub = sign.generate_public_key(priv)

    ser_priv = sign.serialize_private_key(priv, password)
    ser_pub = sign.serialize_public_key(pub)

    now = datetime.now()
    now = now.strftime("%Y%m%d_%H%M%S")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    projeto_dir = os.path.abspath(os.path.join(current_dir, ".."))
    pasta_pub = os.path.abspath(os.path.join(projeto_dir, "pub"))
    pasta_priv = os.path.abspath(os.path.join(projeto_dir, "priv"))

    pub_path = os.path.join(pasta_pub, f"{now + '-pub.pem'}")

    if not os.path.exists(pasta_pub):
        os.makedirs(pasta_pub)

    with open(pub_path, "wb+") as f:
        f.write(ser_pub)

    priv_path = os.path.join(pasta_priv, f"{now + '-priv.pem'}")

    if not os.path.exists(pasta_priv):
        os.makedirs(pasta_priv)

    with open(priv_path, "wb+") as f:
        f.write(ser_priv)

    # Clearing password from memory
    for i in range(0, len(password)):
        password[i] = 0

    return

# Signs a document
def sign_file(password : bytearray, file_path,priv_path) -> bytes:
    with open(priv_path, "rb") as f:
        priv = sign.load_private_key(f, password)

    with open(file_path, "rb") as f:
        signature = sign.sign(priv, f)

    for i in range(len(password)):
        password[i] = 0

    sig_path = file_path + ".sig"
    with open(sig_path, "wb") as sig_file:
        sig_file.write(signature)

def verify_file(file_path,sig_path,pub_path) -> bool:
    with open(pub_path, "rb") as f:
        pub = sign.load_public_key(f)

    with open(file_path, "rb") as f, open(sig_path, "rb") as s:
        signature = s.read()
        result = sign.verify(pub, f, signature)

    return result