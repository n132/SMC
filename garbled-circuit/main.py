import yao
import util

from abc import ABC

class Garbler:
    def __init__(self, FILE):
        parsed = util.parse_json(FILE)
        self.name = parsed["name"]
        circuit = parsed["circuits"][0]

        garbled_circuit = yao.GarbledCircuit(circuit)
        pbits = garbled_circuit.get_pbits()

        self.circuitEntry = {
            "circuit": circuit,
            "garbled_circuit": garbled_circuit,
            "garbled_tables": garbled_circuit.get_garbled_tables(),
            "keys": garbled_circuit.get_keys(),
            "pbits": pbits,
            "pbits_out": {w: pbits[w] for w in circuit["out"]}
        }
        


testG = Garbler("million.json")

circuit = testG.circuitEntry["circuit"]
pbits = testG.circuitEntry["pbits"]
keys = testG.circuitEntry["keys"]
pbits_out = testG.circuitEntry["pbits_out"]
gtables = testG.circuitEntry["garbled_tables"] # garbled tables
outputs = circuit["out"]

print("gtables:",gtables)
print()
print("keys:", keys)

# generate input dictionaries
a_inputs = {}
b_inputs = {}

awires = circuit.get("alice", [])
bwires = circuit.get("bob", [])
print("awires: ",awires)
print("bwires: ",bwires)
N = len(awires) + len(bwires)


"""
for bits in [format(n, 'b').zfill(N) for n in range(2**N)]:
    bits_a = [int(b) for b in bits[:len(awires)]]  # Alice's inputs
    bits_b = [int(b) for b in bits[N - len(awires):]]  # Bob's inputs

    #print("bits_a:", bits_a)
    #print("bits_b:", bits_b)

    # Map Alice's wires to (key, encr_bit)
    for i in range(len(awires)):
        a_inputs[awires[i]] = (keys[awires[i]][bits_a[i]],
                                pbits[awires[i]] ^ bits_a[i])

    # Map Bob's wires to (key, encr_bit)
    for i in range(len(bwires)):
        b_inputs[bwires[i]] = (keys[bwires[i]][bits_b[i]],
                                pbits[bwires[i]] ^ bits_b[i])

    result = yao.evaluate(circuit, gtables, pbits_out, a_inputs,
                            b_inputs)

    # Format output
    str_bits_a = ' '.join(bits[:len(awires)])
    str_bits_b = ' '.join(bits[len(awires):])
    str_result = ' '.join([str(result[w]) for w in outputs])

    print(f"  Alice{awires} = {str_bits_a} "
            f"Bob{bwires} = {str_bits_b}  "
            f"Outputs{outputs} = {str_result}")
"""


bits_a = [0,0]  # Alice's inputs
bits_b = [0,1]  # Bob's inputs

# Map Alice's wires to (key, encr_bit)
for i in range(len(awires)):
    a_inputs[awires[i]] = (keys[awires[i]][bits_a[i]],
                            pbits[awires[i]] ^ bits_a[i])

# Map Bob's wires to (key, encr_bit)
for i in range(len(bwires)):
    b_inputs[bwires[i]] = (keys[bwires[i]][bits_b[i]],
                            pbits[bwires[i]] ^ bits_b[i])

result = yao.evaluate(circuit, gtables, pbits_out, a_inputs,
                        b_inputs)

# Format output
str_bits_a = ' '.join([str(bits_a[a]) for a in bits_a])
str_bits_b = ' '.join([str(bits_b[a]) for a in bits_b])
str_result = ' '.join([str(result[w]) for w in outputs])

print(f"Alice{awires} = {str_bits_a} "
        f"Bob{bwires} = {str_bits_b}  "
        f"Outputs{outputs} = {str_result}")

