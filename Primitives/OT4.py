# 1-4 OT in GMW according http://people.eecs.berkeley.edu/~sanjamg/classes/cs276-fall14/scribe/lec16.pdf
# n132
import utils
import json
from OT2 import *
from random import randint

def SGnenerator():
    S = []
    for _ in range(6):
        S.append(randint(0,1))
    return S
def OT4_Encrypt(S,m):
    assert(len(S)==6 and len(m)==4)
    res=[]
    res.append(
        S[0] ^ S[2] ^ m[0]
    )
    res.append(
        S[0] ^ S[3] ^ m[1]
    )
    res.append(
        S[1] ^ S[4] ^ m[2]
    )
    res.append(
        S[1] ^ S[5] ^ m[3]
    )
    return res

def OT4_Sender(message,client):
    S = SGnenerator()
    enc = OT4_Encrypt(S,message)
    assert(len(enc)==4)
    # get 4 encoded data(enc) and keys(S)
    client.send(b"n132-OT4")
    try:
        #Si
        OT_Sender([long_to_bytes(S[0]),long_to_bytes(S[1])],client)
    except:
        print("[!] Disconnect: OT4-0")
        return -1
    try:
        #Sj
        OT_Sender([long_to_bytes(S[2]),long_to_bytes(S[3])],client)
    except:
        print("[!] Disconnect: OT4-1")
        return -1
    try:
        #Sk
        OT_Sender([long_to_bytes(S[4]),long_to_bytes(S[5])],client)
    except:
        print("[!] Disconnect: OT4-2")
        return -1
    try:
        # encrypted data
        data = client.recv(3)
        assert(data == b"OT4")
        #print("Sending ENCed list")
        enc= json.dumps(enc).encode()
        client.send(enc)
        return 1
    except:
        print("[!] Disconnect: OT4-3")
        return -1
    
def OT4_Receiver(choice,server):
    assert(choice<4 and choice>=0)
    c = [choice//2,choice%2 ] 
    m= server.recv(8)
    if(m==b"n132-OT4"):
        S0 = bytes_to_long(
            OT_Receiver(c[0],server)
            )
        if(c[0]==0):
            S1 = bytes_to_long(
                OT_Receiver(c[1],server)
                )
            bytes_to_long(
                OT_Receiver(randint(0,1),server)
                )#this number is useless
            
        else:
            bytes_to_long(
                OT_Receiver(randint(0,1),server)
                )#this number is useless
            S1 = bytes_to_long(
                OT_Receiver(c[1],server)
                )
        
        server.send(b"OT4")
        enc= json.loads(server.recv(1024))
        #print(enc)
        result = enc[choice] ^ S0 ^ S1
        return result
    else:
        server.close()
        return -1
# 1-2 OT is reconstructed from the OT I build several days ago-


if __name__ == '__main__':
    OT4_Sender()