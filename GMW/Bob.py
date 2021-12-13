from os import times
from OT4 import *
from GMW import *
import sys
PORT = 6999
def Bob_OT2(cmd):
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, PORT))
    res= OT_Receiver(cmd,s)
    s.close()
    return res
def Bob_OT4(cmd):
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, PORT))
    res= OT4_Receiver(cmd,s)
    s.close()
    return res
def Bob_GMW(data):
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, PORT))
    res= GMW_Reveiver(data,s)
    s.close()
    return res
if __name__ != "__main__":
    ct = 0 
    for x in range(1000):
        exp = randint(0,1)
        if(exp != int(Bob_OT2(exp)[-1:])):
            ct +=1
    print((1000-ct)/1000)
if __name__ != "__main__":
    ct = 0 
    test = [0,1,1,0]
    for x in range(1000):
        exp = randint(0,3)
        if(test[exp] != Bob_OT4(exp)):
            ct +=1
    print((1000-ct)/1000)
if __name__ != "__main__":
    ct = 0
    import time
    t = time.time()
    for x in range(100):
        tmp = []
        for y in range(8):
            tmp.append(randint(0,1))
        res=Bob_GMW(tmp)
        oracle = (tmp ==[1,0,0,1,1,1,0,0])
        if(res== oracle):
            ct +=1
    print(time.time()-t)
    print(ct)
if __name__ =='__main__':
    if(len(sys.argv)!=2):
        print("[*] Usage: python3 Bob.py [inputs]")
        print("[*] Example: python3 Bob.py [0,1,1,0,1,1,1,0]")
    else:
        inputs = json.loads(sys.argv[1])
        #print(res)
        print("[*] Running Circuit: ",CIR)
        res=Bob_GMW(inputs)
        print("[+] The result is ",res)