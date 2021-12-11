# n132
# How to play any mental game, or a completeness theorem for protocols with honest majority
# GMW 87
import json
from os import close
from random import choice
from OT4 import *
def GMW_SPLITER(inputs):
    # input is a list of 0,1
    A = []
    B = []
    for x in inputs:
        A.append(randint(0,1))
        B.append(A[-1]^x)
    return A,B
def ReceiveANum(client):
    try:
        num= int(client.recv(1024))
        return num
    except:
        return -1
def GMW_X(skt):# x's solutiin: a untrusted third party could help calculation
    n1 = ReceiveANum(skt)
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, 1026))
    s.listen(5)
    skt2,addr = s.accept()
    n2 = ReceiveANum(skt2)
    skt2.close()
    if(n1==-1 or n2 ==-1):
        exit(1)
    res = n1 ^ n2
    skt.send(res)
    skt.close()
    return 1   
def GMW_Reveiver(inputs,skt):# Bob
    A2,B2 = GMW_SPLITER(inputs)
    if(skt.recv(8)==b"n132-GMW"):
        # B-exchange
        skt.send(json.dumps(A2).encode())
        B1 = json.loads(skt.recv(1024))#$?

        # ----- Bob's shares: B1 B2 
        # receive the circuit
        cir = json.loads(skt.recv(1024))
        #print(circuit)
        skt.send("go!")

        share = B1+B2
        res = evaluateClient(skt,cir,inputs,share)
        return res
    else:
        return -1
# request
def GMW_Sender(inputs,skt):# Alice
    # B- exchange
    A1,B1 = GMW_SPLITER(inputs)
    skt.send(b"n132-GMW")
    A2 = json.loads(skt.recv(1024))
    skt.send(json.dumps(B1).encode())
    #------ Alice's shares: A1 A2
    # send the circuit
    with open("./Gequal.json") as f:
        circuit = f.read()
    
    skt.send(circuit.encode())
    circuit = json.loads(circuit)
    # send the data to the calculator-x
    if(b"go!" != skt.recv(3)):
        exit(1)
    share = A1 + A2
    res = evaluateServer(skt,circuit,inputs,share)
    #print(res)
    return res
def req_x(num,skt,id):
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, 1025))
    s.send(str(num).encode())
    data ={
        "type":"Y",
        "id":id
    }
    # request client
    skt.send(json.dumps(data))
    if(skt.recv(3)!=b"XxX"):
        exit(1)
    res = int(s.recv(1024))
    s.close()
    return res
def req_y(myshare):
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, 1026))
    s.send(str(myshare).encode())
    s.close()
    return 1
def XOR_Request(skt,gate,share):
    myshare = share[gate['input'][0]] ^ share[gate['input'][1]]
    # request X + request Client 
    res = req_x(myshare,skt,gate['id'])
    return res
def NOX(skt,id):
    data ={
        "type": "X",
        "id": id
    }
    skt.send(json.dumps(data))
    if(skt.recv(3)!=b"XxX"):
        exit(1)
    return 1
    #print(id)#request
def AND_Request(skt,gate,share):
    data={
        "type": "Y",
        "id": gate['id']
    }
    skt.send(json.dumps(data))

    choice = (share[gate['input'][0]]<1)+share[gate['input'][1]] 
    res = OT4_Receiver(choice,skt)
    res = req_x(res,skt,-1)
    return res 
def evaluateServer(skt,cir,data,share):
    assert(len(data)==len(cir['S-inputs']))
    gates= cir['gates']
    pool = [-1] * (cir['output'][0]+1)
    s_in = cir['S-inputs']
    # init data pool
    for _ in range(len(s_in)):
        pool[s_in[_]] = data[_]
    #print(pool)
    for x in gates:
        logic = x['type']
        if(logic == 'NOT'):
            if(pool[x['input'][0]]!=-1):#NOT_LOC
                pool[x['output'][0]]= (pool[x['input'][0]]+1)%2
            else:
                NOX(skt,x['id'])
        elif(logic == "XOR"):
            if(pool[x['input'][0]]!=-1 and pool[x['input'][1]]!=-1):#XOR_LOC
                pool[x['output'][0]]= pool[x['input'][0]] ^ pool[x['input'][1]]
            elif(pool[x['input'][0]]!=-1 or pool[x['input'][1]]!=-1):
                pool[x['output'][0]] = XOR_Request(skt,x,share)
            else:
                NOX(skt,x['id'])
        elif(logic == "AND"):
            if(pool[x['input'][0]]!=-1 and pool[x['input'][1]]!=-1):#AND_LOC
                pool[x['output'][0]]= pool[x['input'][0]] & pool[x['input'][1]]
            elif(pool[x['input'][0]]!=-1 or pool[x['input'][1]]!=-1):
                pool[x['output'][0]]= AND_Request(skt,x,share)
            else:
                NOX(skt,x['id'])
        else:
            exit(1)
    data={
        "result": pool[-1],
        "id": 0x6999
    }
    skt.send(json.dumps(data))
    return pool[-1]
def evaluateClient(skt,cir,data,share):
    gates= cir['gates'] 
    pool = [-1] * (cir['output'][0]+1)
    c_in = cir['C-inputs']

    for _ in range(len(c_in)):
        pool[c_in[_]] = data[_]
    
    while(1):
        data = json.loads(skt.recv(1024))
        if(data['id']==0x6999):
            break
        tmp = gates[data['id']]
        if(data["type"]=="X"):
            assert( [x for x in tmp["inputs"] if pool[x] == -1 ]==[])
            #make sure we have all the inputs
            if(tmp['type']=="NOT"):
                pool[tmp['output'][0]]= (pool[tmp['input'][0]]+1)%2
            elif(tmp['type']=="XOR"):
                pool[tmp['output'][0]]= pool[tmp['input'][0]] ^ pool[tmp['input'][1]]
            elif(tmp['type']=='AND'):
                pool[tmp['output'][0]]= pool[tmp['input'][0]] & pool[tmp['input'][1]]
            else:
                exit(1)
            skt.send(b"XxX")
        elif(data['type']=='Y'):
            if(tmp['type']=="XOR"):
                myshare = share[ tmp['input'][0] ] ^ share[ tmp['input'][1] ]
                req_y(myshare)
                skt.senc(b"XxX")
            elif(tmp['type']=="AND"):
                myshare = [share[tmp['input'][0]], share[tmp['input'][1]]]
                table = tableMaker(myshare)
                alpha = randint(0,1)
                enc_table = [(x^alpha) for x in table]
                OT4_Sender(enc_table,skt)
                data = json.dumps(skt.recv(1024))['id']
                if(data==-1):
                    req_y(alpha)
                    skt.senc(b"XxX")
                else:
                    exit(-1)

        else:
            exit(1)
    return data['result']
def tableMaker(share):
    res = []
    for x in range(2):
        for y in range(2):
            tmp = (x ^ share[0]) & (y ^ share[1])
            res.append(tmp)
    return res

if __name__ == '__main__':
    with open("./Gequal.json") as f:
        circuit = f.read()
    cir  = json.loads(circuit)
    evaluateServer(0,cir,[0,1])