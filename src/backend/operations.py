import os
from backend import signature as s

# Generates key pair with a given password
def generate_keys(password : str):
    password_bytes = bytearray(password.encode('utf-8'))

    priv = s.generate_private_key()
    pub = s.generate_public_key(priv)

    ser_priv = s.serialize_private_key(priv, bytes(password_bytes))
    ser_pub = s.serialize_public_key(pub)

    # Saving .pem files
    pub_path = os.path.join("keys", "pub.pem")
    with open(pub_path, "wb") as f:
        f.write(ser_pub)

    priv_path = os.path.join("keys", "priv.pem")
    with open(priv_path, "wb") as f:
        f.write(ser_priv)

    # Clearing password from memory
    for i in range(0, len(password_bytes)):
        password_bytes[i] = 0
    
    return

# ss a document
def s(password : str, file_path):
    priv_path = os.path.join("keys", "priv.pem")
    priv = s.load_private_key(priv_path, password.encode('utf-8'))
    with open(file_path, "rb") as f:
        sature = s.sign(priv, f)

    sig_path = file_path + ".sig"
    with open(sig_path, "wb") as sig_file:
        sig_file.write(sature)

    print(f"sature saved to {sig_path}")