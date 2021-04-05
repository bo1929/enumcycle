import os
from collections import Counter

pref_cycles = "../results/"
pref_times = "../results/time_results"

n_thd = [2, 4, 8]
graph_names = ['GD02_a', 'GD02_b', 'ibm32']
methods = ['E1', 'E2', 'E3']

cycle_lengths_all = {}
cycle_enum_all = {}

for m in methods:
    cycle_lengths_all[m] = {gn: [] for gn in graph_names}
    cycle_enum_all[m] = {gn: [] for gn in graph_names}

# cycle_lengths_all = {
#     "E1": {"GD02_a": [], "GD02_b": [], "ibm32": []},
#     "E2": {"GD02_a": [], "GD02_b": [], "ibm32": []},
#     "E3": {"GD02_a": [], "GD02_b": [], "ibm32": []},
# }
# cycle_enum_all = {
#     "E1": {"GD02_a": [], "GD02_b": [], "ibm32": []},
#     "E2": {"GD02_a": [], "GD02_b": [], "ibm32": []},
#     "E3": {"GD02_a": [], "GD02_b": [], "ibm32": []},
# }

for m in cycle_lengths_all.keys():
    for gn in cycle_lengths_all[m]:
        with open(os.path.join(pref_cycles, gn + "_" + m + ".out")) as f:
            for line in f:
                cycle_lengths_all[m][gn].append(len(line.split(" ")[:-1]))
                cycle_enum_all[m][gn].append(line)
        cycle_enum_all[m][gn].sort()

for gn in cycle_enum_all["E1"].keys():
    sorted_e1 = cycle_enum_all['E1'][gn]
    sorted_e2 = cycle_enum_all['E2'][gn]
    sorted_e3 = cycle_enum_all['E3'][gn]

    if len(sorted_e1) != len(sorted_e2) or len(sorted_e1) != len(sorted_e3):
        raise ValueError(f"Results are different! {len(sorted_e1)}, {len(sorted_e2)}, {len(sorted_e3)}")
    for i in range(len(sorted_e1)):
        if sorted_e1[i] != sorted_e2[i] or sorted_e1[i] != sorted_e3[i]:
            print(f"{sorted_e1[i]}, {sorted_e2[i]}, {sorted_e3[i]}")
            raise ValueError("Results are different!")

print("Sanity check is completed! Results are correct and consistent!\n") 

cycleL = {gn:{} for gn in graph_names}

# cycleL = {
#     "GD02_a": {},
#     "GD02_b": {},
#     "ibm32": {},
# }

for gn in cycle_lengths_all["E1"].keys():
    cycleL[gn] = Counter(cycle_lengths_all["E1"][gn])

print("Cycle lengths -->")
for gn in cycleL.keys():
    print(f"Graph {gn};")
    for count in sorted(cycleL[gn].keys()):
        print("\t", count, ": ", cycleL[gn][count])

print("\n")
for gn in cycleL.keys():
    print(f"For {gn} max length is {max(cycleL[gn].keys())}.")

for gn in graph_names:
    print("\n")
    for m in methods:
        if m == 'E1':
            list_time = [] 
            with open(os.path.join(pref_times, gn + "_time_" + m + ".txt")) as f:
                for line in f:
                    list_time.append(int(line))
            print(f"{gn} using {m} - avg.time elapsed: {sum(list_time)/len(list_time)}")
        else:
            for thd in n_thd:
                list_time = [] 
                with open(os.path.join(pref_times, gn + "_thd" + str(thd) + "_time_" + m + ".txt")) as f:
                    for line in f:
                        list_time.append(int(line))
                print(f"{gn} using {m} with {thd} threads - avg.time elapsed: {sum(list_time)/len(list_time)}")
