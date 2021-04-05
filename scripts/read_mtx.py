import os
import sys
import scipy.io as io

# import pathlib

# abs_path = pathlib.Path(__file__).parent.absolute()

if len(sys.argv) < 2:
    raise ValueError("No input is given!")
graph_name = sys.argv[1]

if graph_name == "ibm32":
    source_path = os.path.join("../", "input_graphs/mtx/ibm32.mtx")
elif graph_name == "GD02_a":
    source_path = os.path.join("../", "input_graphs/mtx/GD02_a.mtx")
elif graph_name == "GD02_b":
    source_path = os.path.join("../", "input_graphs/mtx/GD02_b.mtx")
else:
    raise ValueError("Unkown input graph")

mtx = io.mmread(source_path)

out_str = ""
for i in range(mtx.shape[0]):
    row = mtx.getrow(i)
    print(f"{i+1} : {row.indices+1}")
    for idx in row.indices:
        out_str += str(idx) + " "
    if row.indices.shape[0] < 1:
        out_str += " "
    out_str = out_str[:-1] + "\n"

with open(os.path.join("../", "input_graphs", graph_name + ".in"), "w") as text_file:
    text_file.write(out_str)
