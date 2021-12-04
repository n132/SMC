import util
from OT import OblivousTransfer as ot
import yao
import json


f = open("./million.json")
circuit = json.load(f)
circuit = json.dumps(circuit)
circuit = json.loads(circuit)
#print(type(circuit["circuits"][0]))
#circuits = util.parse_json(circuits)
#name = "million"
circuit = circuit["circuits"][0]

garbled_circuit = yao.GarbledCircuit(circuit)
pbits = garbled_circuit.get_pbits()
entry = {
    "circuit": circuit,
    "garbled_circuit": garbled_circuit,
    "garbled_tables": garbled_circuit.get_garbled_tables(),
    "keys": garbled_circuit.get_keys(),
    "pbits": pbits,
    "pbits_out": {w: pbits[w] for w in circuit["out"]},
}

to_send = {
    "circuit": entry["circuit"],
    "garbled_tables": entry["garbled_tables"],
    "pbits_out": entry["pbits_out"],
}

socket_a = util.GarblerSocket()
ot_a = ot(socket_a, enabled=True)
socket_a.send_wait(to_send)

circuit, pbits, keys = entry["circuit"], entry["pbits"], entry["keys"]
outputs = circuit["out"]
a_wires = circuit.get("alice", [])  # Alice's wires
a_inputs = {}  # map from Alice's wires to (key, encr_bit) inputs
b_wires = circuit.get("bob", [])  # Bob's wires
b_keys = {  # map from Bob's wires to a pair (key, encr_bit)
    w: ((key0, 0 ^ pbits[w]), (key1, 1 ^ pbits[w]))
    for w, (key0, key1) in keys.items() if w in b_wires
}
N = len(a_wires) + len(b_wires)

print(f"======== {circuit['id']} ========")

# Generate all inputs for both Alice and Bob

bits_a = input("Alice input (format: 0 0):")
bits_a = [int(x) for x in bits_a.split()]
#print("bits_a:", bits_a)

#for bits in [format(n, 'b').zfill(N) for n in range(2**N)]:
    #bits_a = [int(b) for b in bits[:len(a_wires)]]  # Alice's inputs
    #print(len(a_wires))
    

    # Map Alice's wires to (key, encr_bit)
for i in range(len(a_wires)):
    a_inputs[a_wires[i]] = (keys[a_wires[i]][bits_a[i]],
                            pbits[a_wires[i]] ^ bits_a[i])

# Send Alice's encrypted inputs and keys to Bob
result = ot_a.get_result(a_inputs, b_keys)

# Format output
str_bits_a = ' '.join([str(bits_a[a]) for a in bits_a])
#str_bits_b = ' '.join([str(bits_b[a]) for a in bits_b])
str_result = ' '.join([str(result[w]) for w in outputs])

print(f"Outputs{outputs} = {str_result}")