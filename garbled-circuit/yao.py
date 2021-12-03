import pickle
import random
from cryptography.fernet import Fernet

def encrypt(key, data):
    """Encrypt a message.

    Args:
        key: The encryption key.
        data: The message to encrypt.

    Returns:
        The encrypted message as a byte stream.
    """
    f = Fernet(key)
    return f.encrypt(data)


def decrypt(key, data):
    """Decrypt a message.

    Args:
        key: The decryption key.
        data: The message to decrypt.

    Returns:
        The decrypted message as a byte stream.
    """
    f = Fernet(key)
    return f.decrypt(data)


def evaluate(circuit, g_tables, pbits_out, a_inputs, b_inputs):
    """evaluate yao circuit with given inputs
    args:
        circuit: a dict containing circuit specs
        g_tables: the garbled tables
        pbits_out: the pbits of outputs
        a_inputs: dict mapping wires to inputs for Alice
        b_inputs: dict mapping wires to inputs for Bob
    
    return:
        A dict mapping output wires with their result
    """

    gates = circuit["gates"]
    wires_outputs = circuit["out"] #list of output wires
    wire_inputs = {}
    evaluation = {} #result of the valuation

    wire_inputs.update(a_inputs)
    wire_inputs.update(b_inputs)

    # iterate over all the gates
    for gate in sorted(gates, key=lambda g: g["id"]):
        gate_id, gate_in, msg = gate["id"], gate["in"], None
        #If its a NOT gate:
        if(len(gate_in) < 2) and (gate_in[0] in wire_inputs):
            # get input key associated with the gate's input wire
            key_in, encr_bit_in = wire_inputs[gate_in[0]]
            # get encrypted message in the gate's garbled table
            encr_msg = g_tables[gate_id][(encr_bit_in, )]
            msg = decrypt(key_in, encr_msg)
        elif(gate_in[0] in wire_inputs) and (gate_in[1] in wire_inputs): #other gates (2 inputs)
            key_a, encr_bit_a = wire_inputs[gate_in[0]]
            key_b, encr_bit_b = wire_inputs[gate_in[1]]
            encr_msg = g_tables[gate_id][(encr_bit_a, encr_bit_b)]
            msg = decrypt(key_b, decrypt(key_a, encr_msg))
        
        if(msg):
            wire_inputs[gate_id] = pickle.loads(msg)
    
    # all gates evaluated, populate result dict
    for out in wires_outputs:
        evaluation[out] = wire_inputs[out][1] ^ pbits_out[out]
    
    return evaluation


class GarbledGate:
    """ Garbled gate representation
    
    """
    def __init__(self, gate, keys, pbits):
        self.keys = keys
        self.pbits = pbits
        self.input = gate["in"]
        self.output = gate["id"]
        self.gate_type = gate["type"]
        self.garbled_table = {} # the garbled table of the gate
        self.clear_garbled_table = {}

        #create the garbled table according to the gate type

        #dict of gate types > function mapping
        switch = {
            "OR": lambda b1, b2: b1 or b2,
            "AND": lambda b1, b2: b1 and b2,
            "XOR": lambda b1, b2: b1 ^ b2,
            "NOR": lambda b1, b2: not (b1 or b2),
            "NAND": lambda b1, b2: not (b1 and b2),
            "XNOR": lambda b1, b2: not (b1 ^ b2)
        }

        #NOT gate is special because of 1-input
        if(self.gate_type == "NOT"):
            self._gen_garbled_table_not()
        else:
            op = switch[self.gate_type]
            self._gen_garbled_table(op)
    
    def _gen_garbled_table_not(self):
        """create a garbled table for NOT gate"""
        inp, out = self.input[0], self.output

        #for each entry (possible input) in the garbled table
        for encr_bit_in in (0, 1):
            bit_in = encr_bit_in ^ self.pbits[inp] #get original bit
            bit_out = int(not (bit_in)) #flip it
            encr_bit_out = bit_out ^ self.pbits[out] #encrypt bit again with pbit table
            #retrieve related keys
            key_in = self.keys[inp][bit_in]
            key_out = self.keys[out][bit_out]

            #serialize output key along with encrypted bit
            msg = pickle.dumps((key_out, encr_bit_out))
            #encrypt the message
            self.garbled_table[(encr_bit_in, )] = encrypt(key_in, msg)
            self.clear_garbled_table[(encr_bit_in, )] = [(inp, bit_in), (out, bit_out), encr_bit_out]
    
    def _gen_garbled_table(self, op):
        """create a garbled table for a 2-input gate"""
        in_a,in_b, out = self.input[0], self.input[1], self.output
        
        #same structure as NOT gate but with 2 inputs
        for encr_bit_a in (0,1):
            for encr_bit_b in (0,1):
                bit_a = encr_bit_a ^ self.pbits[in_a]
                bit_b = encr_bit_b ^ self.pbits[in_b]
                bit_out = int(op(bit_a, bit_b)) #comput the output according to the gate type
                encr_bit_out = bit_out ^ self.pbits[out]
                #retrive keys
                key_a = self.keys[in_a][bit_a]
                key_b = self.keys[in_b][bit_b]
                key_out = self.keys[out][bit_out]

                msg = pickle.dumps((key_out, encr_bit_out))
                self.garbled_table[(encr_bit_a, encr_bit_b)] = encrypt(key_a, encrypt(key_b, msg))
                self.clear_garbled_table[(encr_bit_a, encr_bit_b)] = [
                    (in_a, bit_a), (in_b, bit_b), (out, bit_out), encr_bit_out
                ]
    
    def print_garbled_table(self):
        """print a clear representation of the table"""
        print(f"GATE: {self.output}, TYPE: {self.gate_type}")
        for k, v in self.clear_garbled_table.items():
            #2 input gate
            if len(k) > 1:
                key_a, key_b, key_out = v[0], v[1], v[2]
                encr_bit_out = v[3]
                print(f"[{k[0]}, {k[1]}]: "
                      f"[{key_a[0]}, {key_a[1]}][{key_b[0]}, {key_b[1]}]"
                      f"([{key_out[0]}, {key_out[1]}], {encr_bit_out})")
            else: #its a not gate
                key_in, key_out = v[0], v[1]
                encr_bit_out = v[2]
                print(f"[{k[0]}] :"
                      f"[{key_in[0]}, {key_in[1]}]"
                      f"([{key_out[0]}, {key_out[1]}], {encr_bit_out})")
    
    def get_garbled_table(self):
        #returns the garbled table
        return self.garbled_table


class GarbledCircuit:
    """ Garbled circuit representation
    
    Args
    """

    def __init__(self, circuit, pbits={}):
        self.circuit = circuit
        self.gates = circuit["gates"]
        self.wires = set()

        self.pbits = {}
        self.keys = {}
        self.garbled_tables = {}

        #get all wire ids from circuit and update wire set list
        for gate in self.gates:
            self.wires.add(gate["id"])
            self.wires.update(set(gate["in"]))
        self.wires = list(self.wires)

        self._gen_pbits(pbits)
        self._gen_keys()
        self._gen_garbled_tables()
    
    def _gen_pbits(self, pbits):
        if pbits:
            self.pbits = pbits
        else:
            self.pbits = {wire: random.randint(0, 1) for wire in self.wires} #generate new pbit for each wire
    
    def _gen_keys(self):
        """generate a pair of keys for each wire."""
        for wire in self.wires:
            self.keys[wire] = (Fernet.generate_key(), Fernet.generate_key())

    def _gen_garbled_tables(self):
        for gate in self.gates:
            garbled_gate = GarbledGate(gate, self.keys, self.pbits)
            self.garbled_tables[gate["id"]] = garbled_gate.get_garbled_table()

    def print_garbled_tables(self):
        """print p-bits and a clear representation of all garbled tables."""
        print(f"===== {self.circuit['id']} =====")
        print(f"P-BITS: {self.pbits}")
        for gate in self.gates:
            garbled_table = GarbledGate(gate, self.keys, self.pbits)
            garbled_table.print_garbled_table()
        print()
    
    def get_pbits(self):
        return self.pbits
    
    def get_garbled_tables(self):
        return self.garbled_tables

    def get_keys(self):
        return self.keys