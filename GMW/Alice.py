from OT4 import *
from GMW import *
import sys
PORT = 6999
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
def Alice_GMW(inputs):
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, PORT))
    s.listen(5)
    while True:
        client,addr = s.accept()
        res = GMW_Sender(inputs,client,CIR)
        client.close()
        return res
        #print(res)
if __name__ != '__main__':
    #Alice_OT2()
    #Alice_OT4()
    Alice_GMW()
if __name__ == "__main__":
    if(len(sys.argv)!=2):
        print("[*] Usage: python3 Alice.py [inputs]")
        print("[*] Example: python3 Alice.py [0,1,1,0,1,1,1,0]")
    else:
        inputs = json.loads(sys.argv[1])
        #print(res)
        print("[*] Running Circuit: ",CIR)
        print("[*] Input: ",inputs)
        res=Alice_GMW(inputs)
        print("[+] The result is ",res)
#Get-Process -Name "python" | Stop-Process