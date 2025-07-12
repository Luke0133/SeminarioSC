import os
from backend import signature as sign

# Generates key pair with a given password
def generate_keys(password : str):
    password_bytes = bytearray(password.encode('utf-8'))

    priv = sign.generate_private_key()
    pub = sign.generate_public_key(priv)

    ser_priv = sign.serialize_private_key(priv, bytes(password_bytes))
    ser_pub = sign.serialize_public_key(pub)

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

# Signs a document
def sign_file(password : str, file_path) -> bytes:
    priv_path = os.path.join("keys", "priv.pem")
    with open(priv_path, "rb") as f:
        priv = sign.load_private_key(f, password.encode('utf-8'))

    with open(file_path, "rb") as f:
        signature = sign.sign(priv, f)

    return signature
    
    # Com a signature retornada, fzr prompt de onde salvar e salvar desse jeito:
    #sig_path = prompt q vc pegou (path inteira + nome do arquivo .sig)
    #sig_path = file_path + ".sig"
    #with open(sig_path, "wb") as sig_file:
    #    sig_file.write(signature)


def verify_file(file_path,sig_path) -> bool:
    pub_path = os.path.join("keys", "pub.pem")
    with open(pub_path, "rb") as f:
        pub = sign.load_public_key(f)

    with open(file_path, "rb") as f, open(sig_path, "rb") as s:
        signature = s.read()
        result = sign.verify(pub, f, signature)

    return result