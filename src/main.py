from backend import operations as op

if __name__ == "__main__":
    op.generate_keys("abc")
    op.sign_file("abc","file.txt")
    print(op.verify_file("file.txt","file.txt.sig"))