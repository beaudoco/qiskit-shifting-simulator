## Imports

from qiskit import *
import argparse
from qiskit.test.mock import FakeAlmaden, FakeVigo, FakeValencia, FakeMelbourne, FakeTokyo
#from qiskit.providers.aer import QasmSimulator
from qiskit import Aer
from qiskit.tools import job_monitor # import
import os
import random
import qiskit.transpiler.coupling as coupling 
#from qiskit.providers.aer.noise import NoiseModel
#import qiskit.providers.aer.noise as noise 
import matplotlib.pyplot as plt
from qiskit.test.mock import FakeVigo, FakeMelbourne, FakeAlmaden, FakeValencia, FakeTokyo, FakeMelbourne
import networkx as nx 
import collections
import random
import openpyxl as xl
from tqdm import tqdm
import time

## Loading account and backend

# QX_TOKEN = "67313723797a8e1e5905db1cd035fe6918ea028b47a6ab963058182756fbfc7f6b72e92b21c668900e83e60d206de10aec97751d91ef74de7fde33f31e4b4e58"
# provider = IBMQ.enable_account(QX_TOKEN)
QX_TOKEN = "929e8951d2081e9da2d290c48fc02a9cbd264affbcfc9669a63af613b630a8d545a504adf27d70a6650bf17dfea2fae9400895cb2f0f9f2e4c68466654505723"

IBMQ.enable_account(QX_TOKEN)
provider = IBMQ.get_provider(hub='ibm-q-research', group='penn-3', project='main')

## Get Coupling map of Melbourne

#backend = Aer.get_backend("ibmq_16_melbourne")
backend = provider.get_backend('ibmq_bogota')
#ackend = FakeMelbourne()
edges = backend.configuration().coupling_map

### Chose the backend
#backend = Aer.get_backend("qasm_simulator") 
#backend = provider.get_backend('ibmq_16_melbourne')
# backend = FakeMelbourne()

## Initializing the Quantum Circuit

#qr = QuantumRegister(14, 'q')
qr = QuantumRegister(5, 'q')
# anc = QuantumRegister(2, 'ancilla')
cr = ClassicalRegister(4, 'c')
qc = QuantumCircuit(qr, cr)

# qc.x(qr[2])
# qc.x(qr[11])

for i in range(50):
    #qc.cx(qr[2], qr[12])
    #qc.barrier(qr[2], qr[12])
    qc.cx(qr[0], qr[1])
    qc.barrier(qr[0], qr[1])
    
#qc.measure(qr[2], cr[0])
#qc.measure(qr[12], cr[1])
qc.measure(qr[0], cr[0])
qc.measure(qr[1], cr[1])

for i in range(50):
    #qc.cx(qr[3], qr[11])
    #qc.barrier(qr[3], qr[11])
    qc.cx(qr[2], qr[3])
    qc.barrier(qr[2], qr[3])

#qc.measure(qr[3], cr[2])
#qc.measure(qr[11], cr[3])
qc.measure(qr[2], cr[2])
qc.measure(qr[3], cr[3])
# print(qc)
# exit()
#qc.draw(output='mpl')

## Executing the Quantum Circuit on a Hardware

max_experiments = 75
circ_list = [qc for i in range(max_experiments)]
# job = execute(circ_list, backend, shots=1024)
job = execute(circ_list, backend, shots=8192, coupling_map=edges)
job_monitor(job) # the line
result = job.result()

t = time.time()

## Save the results in an Excel File

row2 = list(result.get_counts(1).keys())
file_counts = open("counts_{}_close.txt".format(backend), "a")

if not os.path.exists("melbourne_close.xlsx"):
    wb = xl.Workbook()
    ws = wb.active

    row = list(result.get_counts(1).keys())
    row.insert(0, "Backend")
    row.insert(0, "Time")

    ws.append(row)
    print(row2)
else:
    wb = xl.load_workbook(filename = "melbourne_close.xlsx")
    ws = wb.active


for k in tqdm(range(max_experiments)):
    print("*************************************************** \
        ***************************************************")
    print("Circuit Index {} {}".format(k, backend), result.get_counts(k))
    print("*************************************************** \
        ***************************************************")

    file_counts.write("{};{};{}\n".format(t, backend, result.get_counts(k)))

    # val = list(result.get_counts(k).values())
    val = result.get_counts(k)
    row = []
    for i in range(len(row2)):
        row.append(val[row2[i]])
    row.insert(0, str(backend))
    row.insert(0, t)
    ws.append(row)     

wb.save("melbourne_close.xlsx")
file_counts.close()   