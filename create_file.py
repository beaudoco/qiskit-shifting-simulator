## Imports

# import os
# import random
# import networkx as nx 
# import collections
import openpyxl as xl
from tqdm import tqdm
import time
# import matplotlib.pyplot as plt
from qiskit import *
# from qiskit.test.mock import FakeAlmaden, FakeVigo, FakeValencia, FakeMelbourne, FakeTokyo
# from qiskit.providers.aer import QasmSimulator
# import qiskit.transpiler.coupling as coupling 
# from qiskit.providers.aer.noise import NoiseModel
# import qiskit.providers.aer.noise as noise


# row2 = list(result.get_counts(1).keys())
file_counts = open("counts_num_gates_{}_{}_far_close.txt".format(30, "bogota"), "a")

if not os.path.exists("far_close.xlsx"):
    wb = xl.Workbook()
    ws = wb.active

    row = list(result.get_counts(1).keys())
    row.insert(0, "Backend")
    row.insert(0, "Time")

    ws.append(row)
else:
    wb = xl.load_workbook(filename = "melbourne_far_close.xlsx")
    ws = wb.active


for k in tqdm(range(max_experiments)):
    print("*************************************************** \
        ***************************************************")
    print("Circuit Index {} {}".format(k, "bogota"), result.get_counts(k))
    print("*************************************************** \
        ***************************************************")

    file_counts.write("{};{};{}\n".format(t, "bogota", result.get_counts(k)))

    val = result.get_counts(k)
    row = []
    # for i in range(len(row2)):
    #     row.append(val[row2[i]])
    row.insert(0, str("bogota"))
    row.insert(0, t)
    ws.append(row)     

wb.save("melbourne_far_close.xlsx")
file_counts.close()  