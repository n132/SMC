import socket
import json
from GMW import CIR
def dealer():
    # dealer will handler all the  
    # get the circuit
    
    host = socket.gethostname()
    s1 = socket.socket()
    s2 = socket.socket()
    s1.bind((host,2021))
    s2.bind((host,2022))
    s1.listen(5)
    s2.listen(5)
    while True:
        GMWA = None
        GMWB = None
        
        GMWA,addr = s1.accept()
        GMWB,addr = s2.accept()
        with open(CIR) as f:
            data =f.read()
        data = json.loads(data)
        gates = data['gates']
        
        pool = [-1]  * (data['output'][0]+1)
        for x in gates:
            print(x)
            if(x['type']=="NOT"):
                if(pool[x['input'][0]]!=-1):
                    pool[x['output'][0]] = (pool[x['input'][0]] +1 )%2
                else:#remote
                    NOX([GMWA,GMWB],x['id'])
            elif(x['type']=="XOR"):
                if(pool[x['input'][0]]!=-1 and pool[x['input'][1]]!=-1):#XOR_LOC
                    pool[x['output'][0]]= pool[x['input'][0]] ^ pool[x['input'][1]]
                elif(pool[x['input'][0]]!=-1 or pool[x['input'][1]]!=-1):#half
                    die("Invalid Circuit")
                    #NOY([GMWA,GMWB],x['id'])
                else:
                    tmp = NOX([GMWA,GMWB],x['id'])
                    pool[x['output'][0]] = tmp 
            elif(x['type']=="AND"):
                if(pool[x['input'][0]]!=-1 and pool[x['input'][1]]!=-1):#AND_LOC
                    pool[x['output'][0]]= pool[x['input'][0]] & pool[x['input'][1]]
                elif(pool[x['input'][0]]!=-1 or pool[x['input'][1]]!=-1):#half
                    die("Invalid Circuit")
                    #NOY([GMWA,GMWB],x['id'])
                else:
                    tmp = NOX([GMWA,GMWB],x['id'])
                    pool[x['output'][0]] = tmp 
        res = {
            "result": pool[-1],
            "id": -1
        }
        GMWA.send(json.dumps(res).encode())
        GMWB.send(json.dumps(res).encode())
        GMWA.close()
        GMWB.close()
def die(s):
    print("[!] ",s)
    exit(1)

def NOX(skts, id):
    data ={
        "type": "X",
        "id": id
    }
    for skt in skts:
        skt.send(json.dumps(data).encode())
        res = skt.recv(3)
        if(res==b"XxX"):
            return -1
        elif(res==b'YYY'):
            skt.send(b"YYY")
            n1 = json.loads(skt.recv(1024))
            skts[1].send(json.dumps(data).encode())
            assert(skts[1].recv(3)==b"YYY")
            skts[1].send(b"YYY")
            n2 = json.loads(skts[1].recv(1024))
            print(n1,n2)
            return n1^n2
    exit(1)
def NOY(skts, id):
    data ={
        "type": "Y",
        "id": id
    }
    for skt in skts:
        skt.send(json.dumps(data))
        if(skt.recv(3)==b"XxX"):
            return 1
    exit(1)
