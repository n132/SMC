# MPC/SMC

## Module Intro

This repo contains our implemenation of two protocols in SMC(Secure Multi-party Communication).

1. Yao's Garbled Circuit

- Garbled Circuit
    - iLabel: Lable input wires
    - cGarble: Generate garbled circuits
    - gcEval: Evaluate the garbled circuits
- Oblivious Transfer
    - Use Cyclic Group
    - 1 in 2 OT

2. GMW

## Usage

Wrapper (to be added)

## Communication Procedure Intro

1. Yao's Garbled Circuit
- Alice sends Bob the circuit, garbled table, and Alice's inputs
- Bob gets his own inputs through OT
- Bob evaluates the circuit and sends back the result

2. GMW

## Details

Function used to test the protocols: Equality function
Encryption library: Fernet from Python Cryptography


## Reference

- Lecture 10 slides

- Secure Multiparty Computation and Secret Sharing (https://www.cambridge.org/core/books/secure-multiparty-computation-and-secret-sharing/4C2480B202905CE5370B2609F0C2A67A)

- Yao’s Garbled Circuits: Recent Directions and Implementations (https://www.peteresnyder.com/static/papers/Peter_Snyder_-_Garbled_Circuits_WCP_2_column.pdf)

