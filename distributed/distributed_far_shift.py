import openpyxl as xl
from tqdm import tqdm
import time
# import matplotlib.pyplot as plt
from qiskit import *
from copy import deepcopy

## Loading account and backend

# provider = IBMQ.get_provider(hub='ibm-q-research', group='penn-3', project='main')

# QX_TOKEN = "67313723797a8e1e5905db1cd035fe6918ea028b47a6ab963058182756fbfc7f6b72e92b21c668900e83e60d206de10aec97751d91ef74de7fde33f31e4b4e58"
# provider = IBMQ.enable_account(QX_TOKEN)

### Chose the backend

# backend = provider.get_backend('ibmq_bogota')
# backend = FakeMelbourne()
backend = Aer.get_backend("qasm_simulator") 

## Initializing the Quantum Circuit

qr = QuantumRegister(5, 'q')
cr = ClassicalRegister(2, 'c')
qc_close = QuantumCircuit(qr, cr)
qc_far = QuantumCircuit(qr, cr)

num_gates = 4 # change this line
q1, q2 = 3, 4
for i in range(num_gates):
    # prepare close 
    qc_close.cx(qr[0], qr[1])
    qc_close.cx(qr[2], qr[3])
    qc_close.barrier()

    # prepare far 
    qc_far.cx(qr[0], qr[1])
    qc_far.cx(qr[q1], qr[q2])

    qc_far.barrier()
    
qc_close_p2 = deepcopy(qc_close)
qc_far_p2 = deepcopy(qc_far)

# measure for close
qc_close.measure(qr[0], cr[0])
qc_close.measure(qr[1], cr[1])

qc_close_p2.measure(qr[2], cr[0])
qc_close_p2.measure(qr[3], cr[1])

# measure for far
qc_far.measure(qr[0], cr[0])
qc_far.measure(qr[1], cr[1])

qc_far_p2.measure(qr[3], cr[0])
qc_far_p2.measure(qr[4], cr[1])

## Executing the Quantum Circuit on a Hardware

max_experiments = 72
circ_list = []
for i in range(max_experiments):
    circ_list.append(qc_close)
    circ_list.append(qc_close_p2)
    
    circ_list.append(qc_far)
    circ_list.append(qc_far_p2)

# print(circ_list[0])
# print(circ_list[1])
# print(circ_list[2])
# print(circ_list[3])
# exit()

job = execute(circ_list, backend, shots=4096)
result = job.result()

t = time.time()

## Save the results in an Excel File

row2 = list(result.get_counts(1).keys())
file_counts = open("distributed_shots_{}_{}_far.txt".format(num_gates, backend), "a")

if not os.path.exists("distributed_shots_far.xlsx"):
    wb = xl.Workbook()
    ws = wb.active

    row = list(result.get_counts(1).keys())
    row.insert(0, "Backend")
    row.insert(0, "Time")

    ws.append(row)
else:
    wb = xl.load_workbook(filename = "distributed_shots_far.xlsx")
    ws = wb.active
    
