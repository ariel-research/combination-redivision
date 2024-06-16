import pandas, sys, time, experiments_csv
from collections import defaultdict
df = pandas.read_csv('rishon-letzion.csv')
print("Raw table: ", df)

import prtpy
# from prtpy import BinnerKeepingContents, BinnerKeepingSums, printbins, partition

numbins = 0
entitlements = []
items = []
for i in range(len(df.values)):
    if (str(df.values[i][11]) != "nan"):
        numbins = numbins + 1
        entitlements.append(float((df.values[i][11])[:-1]) / 100)
new_entitlements = []
for i in range(len(entitlements)):
    new_entitlements.append((entitlements[i]) / sum(entitlements))

print("Entitlements: ", new_entitlements)

for i in range(len(df.values)):
    items.append(int(df.values[i][3].replace(',', '')))

print("Items: ", items)

count_values = defaultdict(int)
for num in items:
    count_values[num] += 1
count_values = dict(count_values)
print("count_values: ", count_values)

items = list()
copies = list()
for key in count_values.keys():
    items.append(key)
    copies.append(count_values[key])

print("\n ### EXPERIMENT COMPLETE GREEDY ###\n")


# start = time.time()
# prtpy.printbins(prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, 
#     numbins=numbins, items=items, entitlements=new_entitlements, objective=prtpy.obj.MinimizeDistAvg))
# end = time.time()
# print(end - start)
# sys.exit(1)

print("\n ### EXPERIMENT ILP AVG ###\n")

start = time.time()

prtpy.printbins(prtpy.partition(algorithm=prtpy.partitioning.ilp_avg, 
    numbins=numbins, items=items, entitlements=entitlements, copies=copies))

end = time.time()
print(end - start)
