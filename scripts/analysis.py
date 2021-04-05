import os
from collections import Counter

pref_cycles = "../results/"
pref_times = "../results/time_results"

n_thd = [2, 4, 8]

method_results = {
    "E1": {"GD02_a": [], "GD02_b": [], "ibm32": []},
    "E2": {"GD02_a": [], "GD02_b": [], "ibm32": []},
    "E3": {"GD02_a": [], "GD02_b": [], "ibm32": []},
}
for method in method_results.keys():
    for graph_name in method_results[method]:
        with open(os.path.join(pref_cycles, graph_name + "_" + method + ".out")) as f:
            for line in f:
                method_results[method][graph_name].append(len(line.split(" ")[:-1]))

cycle_lens = {
    "GD02_a": {},
    "GD02_b": {},
    "ibm32": {},
}

for graph_name in method_results["E1"].keys():
    cycle_lens[graph_name] = Counter(method_results["E1"][graph_name])

for graph in cycle_lens.keys():
    print(graph)
    for count in sorted(cycle_lens[graph].keys()):
        print("\t", count, ": ", cycle_lens[graph][count])

for graph in cycle_lens.keys():
    print(f"For {graph} max length is {max(cycle_lens[graph].keys())}.")
