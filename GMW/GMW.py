# n132
# How to play any mental game, or a completeness theorem for protocols with honest majority
# GMW 87
import json
from OT4 import *
CIR = "./circuits/Gbig_equal.json"
def GMW_SPLITER(inputs):
    # input is a list of 0,1
    A = []
    B = []
    for x in inputs:
        A.append(randint(0,1))
        B.append(A[-1]^x)
    return A,B
def GMW_Reveiver(inputs,skt):# Bob
    A2,B2 = GMW_SPLITER(inputs)
    if(skt.recv(8)==b"n132-GMW"):
        # B-exchange
        skt.send(json.dumps(A2).encode())
        B1 = json.loads(skt.recv(1024))#$?

        # ----- Bob's shares: B1 B2 
        # receive the circuit
        cir = json.loads(skt.recv(4096))
        skt.send(b"go!")
        B = B1+B2
        share = [0] * len(B)
        order = cir['S-inputs'] +cir['C-inputs']
        for x in range(len(B)):
            share[order[x]] = B[x]
        res = evaluateClient(skt,cir,inputs,share)
        return res
    else:
        return -1
def GMW_Sender(inputs,skt,cir=None):# Alice
    # B- exchange
    A1,B1 = GMW_SPLITER(inputs)
    skt.send(b"n132-GMW")
    A2 = json.loads(skt.recv(1024))
    skt.send(json.dumps(B1).encode())
    #------ Alice's shares: A1 A2
    # send the circuit
    cir = cir or CIR
    with open(cir) as f:
        circuit = f.read()
    skt.send(circuit.encode())
    circuit = json.loads(circuit)
    # send the data to the calculator-x
    if(b"go!" != skt.recv(3)):
        exit(1)
    A = A1 +A2
    share = [0] * len(A)
    order = circuit['S-inputs'] +circuit['C-inputs']
    for x in range(len(A)):
        share[order[x]] = A[x]
    
    res = evaluateServer(skt,circuit,inputs,share)
    return res
def evaluateServer(skt,cir,data,share):
    assert(len(data)==len(cir['S-inputs']))
    gates= cir['gates']
    pool = [-1] * (cir['output'][0]+1)
    s_in = cir['S-inputs']
    # init data pool
    for _ in range(len(s_in)):
        pool[s_in[_]] = data[_]
    
    # connect with dealer
    dealer = socket.socket()
    host = socket.gethostname()
    dealer.connect((host, 2021))
    
    with open(CIR) as f:
        cir =f.read()
    cir = json.loads(cir)
    gates = cir['gates']
    while(True):
        data = json.loads(dealer.recv(1024))
        id = data["id"]
        if(id==-1):
            res = data['result']
            return res
        x = gates[id]
        if(data['type']=='X'):
            if(x['type']=='NOT'):
                if(pool[x['input'][0]]!=-1):
                    pool[x['output'][0]] = (pool[x['input'][0]] +1 )%2
                else:
                    dealer.send(b"---")
            elif(x['type']=='XOR'):
                if(pool[x['input'][0]]!=-1 and pool[x['input'][1]]!=-1):
                    pool[x['output'][0]]= pool[x['input'][0]] ^ pool[x['input'][1]]
                    dealer.send(b"XxX")
                elif(pool[x['input'][0]]!=-1 or pool[x['input'][1]]!=-1):
                    myshare = share[x['input'][0]] ^ share[x['input'][1]]
                    dealer.send(b"YYY")
                    
                    if(dealer.recv(3)==b'YYY'):#confirm
                        
                        dealer.send(json.dumps(myshare).encode())
                    else:
                        exit(1)                    
                else:
                    dealer.send(b"---")
            elif(x['type']=="AND"):
                if(pool[x['input'][0]]!=-1 and pool[x['input'][1]]!=-1):
                    pool[x['output'][0]]= pool[x['input'][0]] & pool[x['input'][1]]
                    dealer.send(b"XxX")
                elif(pool[x['input'][0]]!=-1 or pool[x['input'][1]]!=-1):
                    table = tableMaker([share[x['input'][0]],share[x['input'][1]]])
                    alpha = randint(0,1)
                    encTable = [_^alpha for _ in table]
                    OT4_Sender(encTable,skt)
                    dealer.send(b"YYY")
                    if(dealer.recv(3)==b'YYY'):#confirm
                        dealer.send(json.dumps(alpha).encode())
                    else:
                        exit(1)  
                else:
                    dealer.send(b"---")
            else:
                exit(1)
        else:
            exit(1)
def evaluateClient(skt,cir,data,share):
    assert(len(data)==len(cir['S-inputs']))
    gates= cir['gates']
    pool = [-1] * (cir['output'][0]+1)
    s_in = cir['S-inputs']
    # init data pool
    for _ in range(len(s_in)):
        pool[s_in[_]] = data[_]

    # connect with dealer
    dealer = socket.socket()
    host = socket.gethostname()
    dealer.connect((host, 2022))

    with open(CIR) as f:
        cir =f.read()
    cir = json.loads(cir)
    gates = cir['gates']
    while(True):
        data = json.loads(dealer.recv(1024))
        id = data["id"]
        if(id==-1):
            res = data['result']
            return res
        x = gates[id]
        if(data['type']=='X'):
            if(x['type']=='NOT'):
                if(pool[x['input'][0]]!=-1):
                    pool[x['output'][0]] = (pool[x['input'][0]] +1 )%2
                else:
                    dealer.send(b"---")
            elif(x['type']=='XOR'):
                if(pool[x['input'][0]]!=-1 and pool[x['input'][1]]!=-1):
                    pool[x['output'][0]]= pool[x['input'][0]] ^ pool[x['input'][1]]
                    dealer.send(b"XxX")
                elif(pool[x['input'][0]]!=-1 or pool[x['input'][1]]!=-1):
                    myshare = share[x['input'][0]] ^ share[x['input'][1]]
                    dealer.send(b"YYY")
                    
                    if(dealer.recv(3)==b'YYY'):#confirm
                        dealer.send(json.dumps(myshare).encode())
                    else:
                        exit(1)                    
                else:
                    dealer.send(b"---")
            elif(x['type']=="AND"):
                if(pool[x['input'][0]]!=-1 and pool[x['input'][1]]!=-1):
                    pool[x['output'][0]]= pool[x['input'][0]] & pool[x['input'][1]]
                    dealer.send(b"XxX")
                elif(pool[x['input'][0]]!=-1 or pool[x['input'][1]]!=-1):
                    choice = (share[x['input'][0]]*2)+share[x['input'][1]]
                    enc_res = OT4_Receiver(choice,skt)
                    dealer.send(json.dumps(enc_res))
                    dealer.send(b"YYY")
                    if(dealer.recv(3)==b'YYY'):#confirm
                        dealer.send(json.dumps(enc_res).encode())
                    else:
                        exit(1)
                else:
                    dealer.send(b"---")
            else:
                exit(1)
        else:
            exit(1)
def tableMaker(share):
    res = []
    for x in range(2):
        for y in range(2):
            tmp = (x ^ share[0]) & (y ^ share[1])
            res.append(tmp)
    return res
if __name__ == '__main__':
    pass

