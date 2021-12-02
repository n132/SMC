import socket
import OT
PORT = 6999
from Crypto.PublicKey import ECC

key = ECC.generate(curve='P-256')
if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, PORT))
    try:
        bob = OT("Bob")
    except:
        s.close()