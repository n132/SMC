import json
from random import randint
from cryptography.fernet import Fernet

SWITCH = {
    "AND": lambda x, y: x and y,
    "OR": lambda x, y: x or y,
    "XOR": lambda x, y: x ^ y,
    "NOT": lambda x: not x,
    "NAND": lambda x, y: not (x and y),
    "NOR": lambda x, y: not (x or y),
    "XNOR": lambda x, y: not (x ^ y)
}

def encrypt(key,data):# a little not secure because iv is included in the enc
    return Fernet(key).encrypt(data)

def decrypt(key,data):
    return Fernet(key).decrypt(data)

def genkey():
    return Fernet.generate_key()

# Labels for each wire
def circuitLabels(cinfo):
    """
    cinfo: object with circuit info

    output: list of tuples (k0, k1)
    """

    gates = cinfo["gates"]
    a_inputs = cinfo["a_inputs"]
    b_inputs = cinfo["b_inputs"]
    total_num = len(gates) + len(a_inputs) + len(b_inputs)
    res = []

    for _ in range(total_num):
        res.append( {0: genkey(), 1: genkey()} )
    return res

def garbleCircuit(cinfo, labels):
    """
    cinfo: object with circuit info
    labels: list of key tuples from circuitLabels

    output: a garbled circuit, keys for (0, 1) of output
    """

    gates = cinfo["gates"]
    gc = [] # output list

    for g in gates: # loop through all the gates and add table to gc
        gate = {}
        res = []
        logic = SWITCH[g["type"]]
        if(g["type"] == "NOT"):
            #special case for NOT since it only has 1 input
            for i in range(2):
                g_out = logic(i)
                assert(g_out == 0 or g_out == 1)
                raw_label = labels[g["output"][0]][g_out]
                k0 = labels[g["input"][0]][i]

                tmp = encrypt(k0, raw_label)
                res.append(tmp)
        else:
            for i in range(2):  # loop through inputs and create gate table values
                for j in range(2):
                    # output labels
                    g_out = logic(i,j)
                    assert(g_out == 0 or g_out ==1)
                    #print("",labels[g["output"][0]][g_out], "\n")
                    raw_label = labels[g["output"][0]][g_out]
                    #print(raw_label)
                    # get keys from labels
                    #print("  ", labels[g["input"][0]][i], "\n")
                    k0 = labels[g["input"][0]][i]
                    k1 = labels[g["input"][1]][j]

                    tmp = encrypt(k1, encrypt(k0, raw_label))
                    res.append(tmp)
        
        gate["id"] = g["id"]
        gate["garbledResult"] = res
        gc.append(gate)

    rmap = {
        0: labels[cinfo["output"][0]][0],
        1: labels[cinfo["output"][0]][1]
    }

    return gc, rmap # circuit, result_map

def evalGate(w1, w2, table):
    """
    k0, k1, and a table
    """
    # attempt decryption on all gates
    for g in table:
        try:
            if(w2):
                res=decrypt(w1, decrypt(w2, g))
                if(res):
                    return res
            else:
                res = decrypt(w1, g)
                if(res):
                    return res
        except Exception:
            pass
    # failed to evaluate gate
    print("gate eval failure")
    exit(1)

def evalCircuit(gc, inputs, cinfo, results_map):
    """
    garbledcircuit: a garbled circuit object
    inputs: 
    cinfo: the circuit
    results map: map for result bits.

    output: output bit
    """
    assert(len(inputs) == len(cinfo["a_inputs"])) + len(cinfo["b_inputs"])
    inputs += [0] * (cinfo["output"][0] - len(inputs) + 1)
    
    for x in gc:
        '''
        {"id": 0, "garbledResult": [b'xxxxxx, ....]}
        '''
        gatettype = cinfo["gates"][x["id"]]["type"]

        wire1 = inputs[cinfo["gates"][x["id"]]["input"][0]]
        if(gatettype == "NOT"):
            wire2 = None
        else:
            wire2 = inputs[cinfo["gates"][x["id"]]["input"][1]]
        
        output_idx = cinfo["gates"][x["id"]]["output"][0]
        res = evalGate(wire1, wire2, x["garbledResult"])
        inputs[output_idx] = res

    if(results_map[0] == inputs[cinfo["output"][0]]):
        return 0
    else:
        return 1