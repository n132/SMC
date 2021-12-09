import json
from util import *

class Circuit:
    def __init__(self):
        self.circuit = "./million.json"
        self.keys = self.all_key()
        self.pbits = gen_pbits(self.get_num_wires(self.get_circuit()))

    def get_circuit(self):
        f = open(self.circuit)
        circuit = json.load(f)
        circuit = json.dumps(circuit)
        circuit = json.loads(circuit)
        #print(circuit)
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
        self.gates = self.get_circuit()['circuits'][0]['gates']
        print("gates", self.gates)
        self.table = {}
        for gate in self.gates:
            garbled_gate = GarbledGate(gate, self.pbits, self.keys)
            if gate["type"] == "NOT":
                self.table[gate["id"]] = garbled_gate.gen_garbled_not_gate_table()
            else:
                self.table[gate["id"]] = garbled_gate.gen_garbled_gate_table()
        print("###########table:", self.table)

#circuit = Circuit()
#print(circuit.all_key())

class GarbledGate:
    def __init__(self, gate, pbits, keys):
        print("gate", gate)
        self.op = gate["type"]
        self.a_wire = gate["in"][0]
        if self.op != "NOT":
            self.b_wire = gate["in"][1]
        self.out_wire = gate["id"]
        self.keys = keys
        self.pbits = pbits

    def gen_garbled_not_gate_table(self):
        table = [[0, 0]] # garbled table
        for a in range(2):
            in_a = a ^ self.pbits[self.a_wire]
            
            res = not in_a
            out = res ^ self.pbits[self.out_wire]

            enc_out = json.dumps({ 'key': self.keys[self.out_wire][out].decode('utf-8'), 'out': out })
            print(type(enc_out.encode('utf-8')))
            enc_out_a = Fernet(self.keys[self.a_wire][a]).encrypt(enc_out.encode('utf-8'))
            table[0][a] = enc_out_a
        #print("table:", table)
        return table


    def gen_garbled_gate_table(self):
        table = [[0, 0], [0, 0]] # garbled table
        for a in range(2):
            for b in range(2):
                in_a = a ^ self.pbits[self.a_wire]
                in_b = b ^ self.pbits[self.b_wire]
                if self.op == 'AND':
                    res = in_a & in_b
                elif self.op == 'OR':
                    res = in_a | in_b
                elif self.op == 'NAND':
                    res = not(in_a & in_b)
                out = res ^ self.pbits[self.out_wire]

                enc_out = json.dumps({ 'key': self.keys[self.out_wire][out].decode('utf-8'), 'out': out })
                print(type(enc_out.encode('utf-8')))
                enc_out_b = Fernet(self.keys[self.b_wire][b]).encrypt(enc_out.encode('utf-8'))

                enc_out_b_a = Fernet(self.keys[self.a_wire][a]).encrypt(enc_out_b)

                table[a][b] = enc_out_b_a
        #print("table:", table)
        return table




#a = GarbledGate({"id": 5, "type": "NAND", "in": [3, 4]}, [0, 0, 1, 1, 0, 1, 1, 0, 0, 1], circuit.all_key())
#a.gen_garbled_gate_table()

a = Circuit()
a.gen_garbled_table()
