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
def ReceiveANum(client):
    try:
        num= int(client.recv(1024))
        return num
    except:
        return -1
def GMW_X(skt):# x's solutiin: a untrusted third party could help calculation
    #skt.send(b"X1")
    n1 = ReceiveANum(skt)
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, 1026))
    s.listen(5)
    
    skt2,addr = s.accept()
    #skt2.send(b"X2")
    n2 = ReceiveANum(skt2)
    skt2.close()
    if(n1==-1 or n2 ==-1):
        exit(1)
    res = n1 ^ n2
    skt.send(str(res).encode())
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
        cir = json.loads(skt.recv(4096))
        skt.send(b"go!")

        share = B1+B2
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
    share = A1 + A2
    res = evaluateServer(skt,circuit,inputs,share)
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
    data = json.dumps(data).encode()
    skt.send(data)
    if(skt.recv(3)!=b"XxX"):
        exit(1)
    res = int(s.recv(1024))
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
def AND_Request(skt,gate,share):
    data={
        "type": "Y",
        "id": gate['id']
    }
    skt.send(json.dumps(data).encode())
    choice = (share[gate['input'][0]]*2)+share[gate['input'][1]]
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
# def dealer(skt):
#     # dealer will handler all the  
#     # get the circuit
#     while True:
#         GMWA = None
#         GMWB = None

#         s1 = socket.socket()
#         host = socket.gethostname()
#         s1.bind((host,2021))
#         s1.listen(5)
#         GMWA,addr = s1.accept()
        
#         A = json.loads(GMWA.recv(1024))



#         s2 = socket.socket()
#         host = socket.gethostname()
#         s2.bind((host,2022))
#         s2.listen(5)
#         GMWB,addr = s2.accept()
#         B = json.loads(GMWB.recv(1024))

#         with open(CIR) as f:
#             data =f.read()
#         data = json.loads(data)
#         gates = data['gates']

#         pool = [-1]  * data['output'][0] 
#         for gate in gates:
#             if(gate['type']=="NOT"):
#                 if(pool[gate['input'][0]]==-1):
                    
#                 else:
#                     pool[gate['output'][0]] = (pool[gate['input'][0]] +1 )%2
#             elif(gate['type']=="XOR"):
#                 if( pool[gate['input'][0]] )
#             elif(gate['type']=="AND"):
#                 pass
        


    # get people's share
    # perform evaluate
# def evaluation(shares,host=None,port=None):
#     s = socket.socket()
#     host = host or socket.gethostname()
#     port = port or 2046
#     s.connect((host,port))
#     s.send(json.dumps(shares).encode())
#     res = s.recv(1024)
#     return res


# def GMWA(skt,inputs):
#     A1,B1 = GMW_SPLITER(inputs)
#     skt.send(b"n132-GMWX")
#     A2 = json.loads(skt.recv(1024))
#     skt.send(json.dumps(B1).encode())
#     shares = []
#     for x in range(len(A1)):
#         shares.append(A1[x] ^ A2[x])
#     data ={
#         "shares":shares,
#         "ID": "A"
#     }
#     res = evaluation(data,port = 2021)
#     return res



# def GMWB(skt,inputs):
#     A2,B2 = GMW_SPLITER(inputs)
#     if(b"n132-GMWX"==skt.recv(9)):
#         skt.send(json.dumps(A2).encode())
#         B1 = json.loads(skt.recv(1024))
#         shares=[]
#         for x in range(len(B1)):
#             shares.append(B1[x] ^ B2[x])
#         data ={
#             "shares":shares,
#             "ID": "B"
#         }
#         res =evaluation(shares,port = 2022)
#         return res
#     return -1

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
    evaluateServer(0,cir,[0,1],[1,2])

