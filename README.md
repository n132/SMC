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
- Alice sends Bob the circuit, garbled table, and keys for each wire
- Bob evaluates the circuit and sends back the result

2. GMW

## Details

Function used to test the protocols: Equality function


## Reference

- Lecture 10 slides

- Secure Multiparty Computation and Secret Sharing (https://www.cambridge.org/core/books/secure-multiparty-computation-and-secret-sharing/4C2480B202905CE5370B2609F0C2A67A)

