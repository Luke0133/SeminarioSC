import os
from datetime import datetime
from backend import signature as sign

# Generates key pair with a given password
def generate_keys(password : bytearray):
    priv = sign.generate_private_key()
    pub = sign.generate_public_key(priv)

    ser_priv = sign.serialize_private_key(priv, password)
    ser_pub = sign.serialize_public_key(pub)

    # Saving .pem files
    now = datetime.now()
    now = now.strftime("%Y%m%d_%H%M%S")
    pub_path = os.path.join("pub", f"{now + '-pub.pem'}")
    with open(pub_path, "wb") as f:
        f.write(ser_pub)

    priv_path = os.path.join("priv", f"{now + '-priv.pem'}")
    with open(priv_path, "wb") as f:
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