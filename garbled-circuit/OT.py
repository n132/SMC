import util
import pickle
import yao
import hashlib

class OblivousTransfer:
    def __init__(self, socket, enabled=True):
        self.socket = socket
        self.enabled = enabled
    

    # Alice -> Bob
    def get_result(self, a_inputs, b_keys):
        # send Alice's inputs and retrieve Bob's result of evaluation.
        # a_inputs: A dict mapping Alice's wires to (key, encr_bit) inputs.
        # b_keys: A dict mapping each Bob's wire to a pair (key, encr_bit).
        # return: The result of the yao circuit evaluation.

        self.socket.send(a_inputs)

        for _ in range(len(b_keys)):
            w = self.socket.receive() # receive gate ID where to perform OT

            if self.enabled:
                pair = (pickle.dumps(b_keys[w][0]), pickle.dumps(b_keys[w][1]))
                self.ot_garbler(pair)
            else:
                to_send = (b_keys[w][0], b_keys[w][1])
                self.socket.send(to_send)
        
        return self.socket.receive()


    # Bob -> Alice
    def send_result(self, circuit, g_tables, pbits_out, b_inputs):
        # evaluate circuit and send the result to Alice
        # circuit: A dict containing circuit spec
        # pbits_out: pbits of outputs
        # b_inputs: A dict mapping Bob's wires to (clear) input bits

        # map from Alice's wires to (key, encr_bit) inputs
        a_inputs = self.socket.receive()
        # map from Bob's wires to (key, encr_bit) inputs
        b_inputs_encr = {}

        for w, b_input in b_inputs.items():
            self.socket.send(w)

            if self.enabled:
                b_inputs_encr[w] = pickle.loads(self.ot_evaluator(b_input))
            else:
                pair = self.socket.receive()
                b_inputs_encr[w] = pair[b_input]

        result = yao.evaluate(circuit, g_tables, pbits_out, a_inputs, b_inputs_encr)

        # sending back circuit evaluation
        self.socket.send(result)

    def ot_garbler(self, msgs):
        # OT Alice side
        # msgs: a pair (msg1, msg2) to suggest to Bob

        # OT starts
        G = util.PrimeGroup() # initialize a PrimeGroup class
        self.socket.send_wait(G)

        # OT protocol based on Nigel Smart's "Cryptography Made Simple"
        c = G.gen_pow(G.rand_int())
        h0 = self.socket.send_wait(c)
        h1 = G.mul(c, G.inv(h0)) # multiply the two and mod by the generated prime num
        k = G.rand_int()
        c1 = G.gen_pow(k)

        # hash the OT key and xor with msg
        e0 = util.xor_bytes(msgs[0], self.ot_hash(G.pow(h0, k), len(msgs[0]))) 
        e1 = util.xor_bytes(msgs[1], self.ot_hash(G.pow(h1, k), len(msgs[1])))

        self.socket.send((c1, e0, e1))

    def ot_evaluator(self, b):
        # OT Bob side
        # b: Bob's input bit used to select one of Alice's msgs
        # return: the msg selected by Bob

        # OT starts
        G = self.socket.receive()
        self.socket.send(True)

        c = self.socket.receive() # receive h0?
        x = G.rand_int()
        x_pow = G.gen_pow(x)
        h = (x_pow, G.mul(c, G.inv(x_pow))) # c/x_pow
        c1, e0, e1 = self.socket.send_wait(h[b])
        e = (e0, e1)
        ot_hash = self.ot_hash(G.pow(c1, x), len(e[b]))
        mb = util.xor_bytes(e[b], ot_hash)

        return mb
    
    def ot_hash(self, pub_key, msg_length):
        # hash function for OT keys
        #print("public key:", pub_key, "msg_length:", msg_length)
        key_length = (pub_key.bit_length() + 7) // 8
        bytes = pub_key.to_bytes(key_length, byteorder="big")
        return hashlib.shake_256(bytes).digest(msg_length)





