import os
import sys

# Adicionar o diretório backend ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, "backend")
sys.path.insert(0, backend_dir)

import operations as op

if __name__ == "__main__":
    password = input("Input password: ")
    op.generate_keys(bytearray(password.encode('utf-8')))

    priv = input("priv: ")
    path = os.path.join("priv", f"{priv}")

    password = input("Input password: ")
    op.sign_file(bytearray(password.encode('utf-8')),"test/file.txt",path)
    
    pub = input("pub: ")
    path = os.path.join("pub", f"{pub}")

    print(op.verify_file("test/file.txt","test/file.txt.sig",path))