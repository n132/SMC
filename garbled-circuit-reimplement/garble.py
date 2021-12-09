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
        #print("gates", self.gates)
        self.table = {}
        for gate in self.gates:
            garbled_gate = GarbledGate(gate, self.pbits, self.keys)
            if gate["type"] == "NOT":
                self.table[gate["id"]] = garbled_gate.gen_garbled_not_gate_table()
            else:
                self.table[gate["id"]] = garbled_gate.gen_garbled_gate_table()
        #print("###########table:", self.table)
        return self.table

#circuit = Circuit()
#print(circuit.all_key())

class GarbledGate:
    def __init__(self, gate, pbits, keys):
        #print("gate", gate)
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
            #print(type(enc_out.encode('utf-8')))
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
                #print(type(enc_out.encode('utf-8')))
                enc_out_b = Fernet(self.keys[self.b_wire][b]).encrypt(enc_out.encode('utf-8'))

                enc_out_b_a = Fernet(self.keys[self.a_wire][a]).encrypt(enc_out_b)

                table[a][b] = enc_out_b_a
        #print("table:", table)
        return table


def degarble(circuit, table, pbits, in_a, in_b):
    # Put all inputs in one
    in_all = {}
    for gate_id in in_a:
        in_all[gate_id] = in_a[gate_id]
    for gate_id in in_b:
        in_all[gate_id] = in_b[gate_id]
    print(in_all)

    gate_list = circuit["circuits"][0]["gates"]
    for gate in gate_list:
        print("gate:", gate["type"])
        if gate["type"] == "NOT":
            in_wire = gate["in"][0]
            bit_in = in_all[in_wire][1]^pbits[in_wire]
            key_in = in_all[in_wire][0]
            out_info = table[gate["id"]][bit_in]
            d = Fernet(key_in)
            out_info = d.decrypt(out_info)
            out_info = json.loads(out_info)
            #print("out_info:", out_info)
        else:
            in_wire_a = gate["in"][0]
            in_wire_b = gate["in"][1]
            
            key_in_a = in_all[in_wire_a][0]
            key_in_b = in_all[in_wire_b][0]
            bit_in_a = in_all[in_wire_a][1]^pbits[in_wire_a]
            bit_in_b = in_all[in_wire_b][1]^pbits[in_wire_b]
            #print("debug", type(in_all[in_wire_b][1]))
            #print(table[gate["id"]][bit_in_a])
            #print(bit_in_b)
            out_info = table[gate["id"]][bit_in_a][bit_in_b]
            d = Fernet(key_in_a)
            out_info = d.decrypt(out_info)
            d = Fernet(key_in_b)
            out_info = d.decrypt(out_info)
            
            out_info = json.loads(out_info)
            #print("out_info:", out_info)
            
        print(out_info)
        #out_info = json.dumps(out_info)
        in_all[gate["id"]] = (out_info["key"], out_info["out"])
        print(in_all)
    
    print(in_all)






#a = GarbledGate({"id": 5, "type": "NAND", "in": [3, 4]}, [0, 0, 1, 1, 0, 1, 1, 0, 0, 1], circuit.all_key())
#a.gen_garbled_gate_table()

a = Circuit()
table = a.gen_garbled_table()

