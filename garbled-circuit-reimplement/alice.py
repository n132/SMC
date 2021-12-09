import zmq
import util
from garble import *

socket = zmq.Context().socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


# Initialize a new circuit
a = Circuit()
circuit = a.get_circuit()
table = a.gen_garbled_table()
#print("table:", table)
pbits = a.pbits
keys = a.keys

# Alice send circuit, garbled table and pbits
socket.send_pyobj({
            "circuit": circuit,
            "table": table,
            "pbits": pbits
            })
print("alice receive reply:", socket.recv())

# Get Alice inputs
bits_a = input("Alice input (format: 0 0):")
bits_a = [int(x) for x in bits_a.split()]

# Map Alice key and input to each wire
a_in_wire_map = {}
cur_bit_a = 0
for each_a_wire in circuit["circuits"][0]["alice"]:
    a_in_wire_map[each_a_wire] = (keys[each_a_wire][bits_a[cur_bit_a]], pbits[each_a_wire]^bits_a[cur_bit_a])
    cur_bit_a += 1
socket.send_pyobj(a_in_wire_map)
socket.recv()

# Set ot 
useOT = False

# Send Bob his key to each input wire
b_wires = circuit["circuits"][0]["bob"]
if useOT == False:
    for each_b_wire in b_wires:
        print(each_b_wire)
        socket.send_pyobj((keys[each_b_wire][0], keys[each_b_wire][1]))
        socket.recv()
else:
    pass

socket.send(b"What's the result?")





#message = socket.recv()
#print("alice received reply [ %s ]" % (message))

