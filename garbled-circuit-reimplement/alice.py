import zmq
import util
from garble import *

socket = zmq.Context().socket(zmq.REQ)
socket.connect("tcp://localhost:5555")



a = Circuit()
circuit = a.get_circuit()
table = a.gen_garbled_table()
pbits = a.pbits

# Alice send circuit, garbled table and pbits
socket.send_pyobj({
            "circuit": circuit,
            "table": table,
            "pbits": pbits
            })

            

message = socket.recv()
print("alice received reply [ %s ]" % (message))

