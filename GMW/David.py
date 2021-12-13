from OT4 import *
from GMW import *
from Dealer import *
import sys
def X():#Xiang's solution
    while True:
        try:
            GMW_X()
        except:
            pass
def XxX():
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host,1025))
    s.listen(5)
    while True:
        client,addr = s.accept()
        GMW_X(client)
        client.close()
if __name__ == "__main__":
    if(len(sys.argv)!=1):
        print("[*] Usage: python3 David.py")
    else:
        dealer()