# n132
# How to play any mental game, or a completeness theorem for protocols with honest majority
# GMW 87
import json
from OT4 import *

def initGMW(info):
    pass
def evaluate():
    pass

def main():
    pass
def GMW_Sender(inputs,skt):# Alice
    # B- exchange
    A1,B1 = GMW_SPLITER(inputs)
    skt.send(b"n132-GMW")
    A2 = json.loads(skt.recv(1024))
    skt.send(json.dumps(B1).encode())
    #------ Alice's shares: A1 A2
    # send the circuit
    with open("./Gequal.json") as f:
        data = f.read()
    data = json.loads(data)
    skt.send()

def GMW_Reveiver(inputs,skt):# Bob
    A2,B2 = GMW_SPLITER(inputs)
    if(skt.recv(8)==b"n132-GMW"):
        # B-exchange
        skt.send(json.dumps(A2).encode())
        B1 = json.loads(skt.recv(1024))#$?
        
        # ----- Bob's shares: B1 B2 
        # receive the circuit
        return 1
    else:
        return -1

def GMW_SPLITER(inputs):
    # input is a list of 0,1
    A = []
    B = []
    for x in inputs:
        A.append(randint(0,1))
        B.append(A[-1]^x)
    return A,B

if __name__ == '__main__':
    initGMW([0,0,1,1,1])