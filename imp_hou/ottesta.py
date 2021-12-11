from cgarbl import *
import gcot
import pickle
from random import randint
from utils import *

# client receives secrets from server
def ottest1():
    s = connect()
    res = gcot.OT_Receiver(0, s)
    print(res)

# cgarbl socket test
def cgarbtesta():
    with open("./equal.json") as f:
        data = f.read()
    
    cinfo = json.loads(data)
    lb = circuitLabels(cinfo)
    gc, rmap = garbleCircuit(cinfo, lb)

    araw = [randint(0,1) for i in range(2)]
    ains = [lb[0][araw[0]], lb[1][araw[1]]] # grab keys for alice inputs
    gcinfo = {
        "gc": gc,
        "cinfo": cinfo,
        "inputs": ains,
        "rmap": rmap,
        "raw_ins": araw
    }
    #print(gcinfo)

    # need to serialize gc and send to bob
    s = connect()
    s.sendall(pickle.dumps(gcinfo)) # send all info to bob

    OTDone = False
    innum = 0
    b_secrets = {0: lb[2], 1: lb[3]}
    print("b_secrets", b_secrets)
    msg = s.recv(256)
    while(not OTDone):
        print("secrets to send:",b_secrets[innum])
        otres = gcot.OT_Sender(b_secrets[innum], s)
        print("ot ended with", otres)
        if(otres == 1):
            innum+=1
        bres = s.recv(256)
        if(bres == b'ins-done'):
            OTDone = True
    
    msg = s.recv(4)
    result = int.from_bytes(msg, 'big')
    print("RESULT:", result)

def singlegatetesta():
    # cgarbl socket test
    with open("./NOR.json") as f:
        data = f.read()
    
    cinfo = json.loads(data)
    lb = circuitLabels(cinfo)
    gc, rmap = garbleCircuit(cinfo, lb)

    araw = [randint(0,1) for i in range(2)]
    ains = [lb[0][araw[0]], lb[1][araw[1]]] # grab keys for alice inputs
    gcinfo = {
        "gc": gc,
        "cinfo": cinfo,
        "inputs": ains,
        "rmap": rmap,
        "raw_ins": araw # nonessential info for correctness testing ONLY
    }
    #print(gcinfo)

    # need to serialize gc and send to bob
    s = connect()
    s.sendall(pickle.dumps(gcinfo)) # send all info to bob

    OTDone = False
    innum = 0
    b_secrets = {0: lb[2], 1: lb[3]}
    print("b_secrets", b_secrets)
    msg = s.recv(256)
    while(not OTDone):
        print("secrets to send:",b_secrets[innum])
        otres = gcot.OT_Sender(b_secrets[innum], s)
        print("ot ended with", otres)
        if(otres == 1):
            innum+=1
        bres = s.recv(256)
        if(bres == b'ins-done'):
            OTDone = True
    
    msg = s.recv(4)
    result = int.from_bytes(msg, 'big')
    print("RESULT:", result)


if(__name__ == "__main__"):
    # ottest1()
    for i in range(1000):
        singlegatetesta()