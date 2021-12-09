import zmq
import time
from garble import *

socket = zmq.Context().socket(zmq.REP)
socket.bind("tcp://*:5555")


while True:
    message = socket.recv_pyobj()

    print("bob received request")
    socket.send(b"ok")

    circuit, table, pbits = message["circuit"], message["table"], message["pbits"]

    bits_b = input("Bob input (format: 0 0):")
    bits_b = [int(x) for x in bits_b.split()]

    b_wires = circuit["circuits"][0]["bob"]

    useOT = False
    a_input_map = socket.recv_pyobj()
    socket.send(b"ok")
    b_input_map = {}
    if useOT == False:
        cur_bit_b = 0
        for each_b_wire in b_wires: 
            b_input_map[each_b_wire] = (socket.recv_pyobj()[bits_b[cur_bit_b]], pbits[each_b_wire]^bits_b[cur_bit_b])
            socket.send(b"ok")
        socket.recv()
        socket.send_pyobj(degarble(circuit, table, pbits, a_input_map, b_input_map))
    else:
        pass

    time.sleep(1)

    