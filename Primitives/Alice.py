import socket
import OT
from Crypto.PublicKey import ECC
PORT = 6999
key = ECC.generate(curve='P-256')


if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, PORT))
    s.listen(5)
    while True:
        c,addr = s.accept()
        try:
            alice = OT("Alice")
        except:
            c.close()
        exit(1)