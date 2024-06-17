import pandas, sys, time, experiments_csv
from collections import defaultdict
from read_input import get_input_from_raw_table
import prtpy, mip, numpy as np

df = pandas.read_csv('rishon-letzion.csv')
print("Raw table: ", df)

def run_ilp_avg_on_part_of_the_data(numrows:int, time_limit:int):
    entitlements, values = get_input_from_raw_table(df.head(numrows))
    total_value = sum(values)
    print(len(values), " values", "\nTotal value = ",total_value)
    print(len(entitlements), " entitlements")

    count_values = defaultdict(int)
    for num in values:
        count_values[num] += 1
    count_values = dict(count_values)
    print(len(count_values), " count_values")
    items = list(count_values.keys())
    copies = list(count_values.values())

    numagents = len(entitlements)
    partition_and_sums = prtpy.partition(algorithm=prtpy.partitioning.ilp_avg,
        numbins=numagents, items=items, entitlements=entitlements, copies=copies,
        outputtype = prtpy.out.PartitionAndSums, solver_name=mip.GRB, time_limit=time_limit)

    balance_payments = [partition_and_sums.sums[i] - entitlement*total_value for i,entitlement in enumerate(entitlements)]
    for i,entitlement in enumerate(entitlements):
        due_value = entitlement*total_value
        print(f"Agent {i} should get {entitlement} = {entitlement*total_value}, and got {partition_and_sums.sums[i]}: {partition_and_sums.lists[i]}. Balance payment: {balance_payments[i]}")
    print("Sum balance payments: ", sum(balance_payments))
    max_balance_payment = max([np.abs(payment) for payment in balance_payments])

    return {"numagents": numagents, "numitems": len(items), "total_value": total_value, "max_balance_payment": max_balance_payment}


print("\n ### EXPERIMENT COMPLETE GREEDY ###\n")


# start = time.time()
# prtpy.printbins(prtpy.partition(algorithm=prtpy.partitioning.complete_greedy, 
#     numbins=numbins, items=values, entitlements=entitlements, objective=prtpy.obj.MinimizeDistAvg))
# end = time.time()
# print(end - start)
# sys.exit(1)

print("\n ### EXPERIMENT ILP AVG ###\n")

ex = experiments_csv.Experiment("results/", "ilp.csv")
# ex.clear_previous_results()

input_ranges = {
    "numrows": range(300,510,10),
    "time_limit": [300, 450],
}

ex.run_with_time_limit(run_ilp_avg_on_part_of_the_data, input_ranges, time_limit=1000)
