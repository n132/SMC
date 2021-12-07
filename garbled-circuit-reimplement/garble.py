import json
from util import *

class Circuit:
    def __init__(self):
        self.circuit = "./million.json"

    def get_circuit(self):
        f = open(self.circuit)
        circuit = json.load(f)
        circuit = json.dumps(circuit)
        circuit = json.loads(circuit)
        print(circuit)
        return circuit

    def get_num_wires(self, circuit):
        return circuit["circuits"][0]["out"][0]

    def all_key(self):
        keys = {}
        num = self.get_num_wires(self.get_circuit())
        for i in range(1, num + 1):
            keys[i] = (gen_key(), gen_key())
        return keys

    def gen_garbled_table(self):
        pass

#circuit = Circuit()
#print(circuit.all_key())

class GarbledGate:
    def __init__(self, op, a_wire, b_wire, pbits):
        self.op = op

    def gen_garbled_gate_table(self):
        for a in range(2):
            for b in range(2):
                in_a = a ^ pbits[a_wire]
                in_b = b ^ pbits[b_wire]
                


        #need key_out and encrypt_bit_out

