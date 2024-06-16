import pandas, sys, time, experiments_csv
from collections import defaultdict
df = pandas.read_csv('rishon-letzion.csv')
print("Raw table: ", df)

import prtpy

numbins = 0
entitlements = []
items = []
for i in range(len(df.values)):
    if (str(df.values[i][11]) != "nan"):
        numbins = numbins + 1
        entitlements.append(float((df.values[i][11])[:-1]) / 100)
sumentitlements = sum(entitlements)
entitlements = [e / sumentitlements for e in entitlements]

print(len(entitlements), " entitlements: ", entitlements)

for i in range(len(df.values)):
    items.append(int(df.values[i][3].replace(',', '')))

print(len(items), " items: ", items)

count_values = defaultdict(int)
for num in items:
    count_values[num] += 1
count_values = dict(count_values)
print(len(count_values), " count_values: ", count_values)

items = list()
copies = list()
for key in count_values.keys():
    items.append(key)
    copies.append(count_values[key])

print("\n ### EXPERIMENT COMPLETE GREEDY ###\n")


# start = time.time()
# prtpy.printbins(prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, 
#     numbins=numbins, items=items, entitlements=entitlements, objective=prtpy.obj.MinimizeDistAvg))
# end = time.time()
# print(end - start)
# sys.exit(1)

print("\n ### EXPERIMENT ILP AVG ###\n")

ex = experiments_csv.Experiment("results/", "ilp.csv")

def run_ilp_avg_on_part_of_the_data(numbins:int):
    partition_and_sums = prtpy.partition(algorithm=prtpy.partitioning.ilp_avg,
        numbins=numbins, items=items, entitlements=entitlements[:numbins], copies=copies,
        outputtype = prtpy.out.PartitionAndSums)
    print(partition_and_sums)
    return {}

input_ranges = {
    "numbins": [10, 20, 30]
}

ex.run_with_time_limit(run_ilp_avg_on_part_of_the_data, input_ranges, time_limit=10)

