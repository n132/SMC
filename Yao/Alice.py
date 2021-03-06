from cgarbl2 import *
import gcot
import pickle
from random import randint
from utils import *
import time

# client receives secrets from server
def ottest1():
    CONSTARTIME = time.time()
    s = connect()
    CONENDTIME = time.time()
    CONTIME = (CONENDTIME - CONSTARTIME)
    rounds = 0
    while(rounds < 5000):
        choice = randint(0,1)
        res = gcot.OT_Receiver(choice, s)
        s.sendall(b'continue')
        rounds += 1
        print(res)
    #print(res)
    return CONTIME
"""
# cgarbl socket test
def cgarbtesta():
    with open("./bigEquals.json") as f:
        data = f.read()
    
    cinfo = json.loads(data)
    lb = iLabel(cinfo)
    gc, rmap = gGarble(cinfo, lb)

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
    print("RESULT:", result) """

def multiintest():
    # cgarbl socket test
    with open("./equal8.json") as f:
        data = f.read()
    
    cinfo = json.loads(data)
    lb = iLabel(cinfo)
    gc, rmap = gGarble(cinfo, lb)

    araw = [randint(0,1) for i in range(len(cinfo["a_inputs"]))]
    ains = ['' for i in range(len(araw))]
    for i in range(len(araw)): # grab keys for alice inputs
        ains[i] = lb[cinfo["a_inputs"][i]][araw[i]]
    gcinfo = {
        "gc": gc,
        "cinfo": cinfo,
        "inputs": ains,
        "rmap": rmap,
        "raw_ins": araw # nonessential info for correctness testing ONLY
    }
    #print(gcinfo)

    # need to serialize gc and send to bob
    CONSTARTIME = time.time()
    s = connect()
    CONENDTIME = time.time()
    CONTIME = (CONENDTIME - CONSTARTIME)
    s.sendall(pickle.dumps(gcinfo)) # send all info to bob

    OTDone = False
    innum = 0
    b_secrets = {}
    for cbin in cinfo["b_inputs"]:
        b_secrets[innum] = lb[cinfo["b_inputs"][innum]]
        innum+=1
    innum = 0
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
    return CONTIME

if(__name__ == "__main__"):
    #ttest1()
    totalcon = 0.0
    for i in range(1000):
        totalcon += multiintest()
    
    print("AVG connection time:", (totalcon / 1000))
