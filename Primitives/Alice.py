from OT4 import *
PORT = 6999
from random import randint

def Alice_OT2():
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, PORT))
    s.listen(5)
    while True:
        client,addr = s.accept()
        OT_Sender([b"This is secret 0",b"This is secret 1"],client)
        client.close()
def Alice_OT4():
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, PORT))
    s.listen(5)
    while True:
        client,addr = s.accept()
        OT4_Sender([0,1,1,0],client)
        client.close()
if __name__ == '__main__':
    #Alice_OT2()
    Alice_OT4()