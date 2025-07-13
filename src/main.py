from backend import operations as op
import os

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