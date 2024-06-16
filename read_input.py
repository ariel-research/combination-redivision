"""
Utility function to parse the input table (in a CSV file) to compute entitlements and values.
"""

import pandas

def get_input_from_raw_table(df:pandas.DataFrame)->tuple:
    entitlements = []
    for i in range(len(df)):
        incoming_relative_ownership = df["in_relative_ownership"][i]
        if (str(incoming_relative_ownership) != "nan"):
            entitlements.append(float(incoming_relative_ownership))
    sumentitlements = sum(entitlements)
    entitlements = [e / sumentitlements for e in entitlements]
    print("sumentitlements = ",sumentitlements)

    values = []
    for i in range(len(df)):
        values.append(int(df["out_due_value_absolute"][i].replace(',', '')))
    return entitlements, values


if __name__=="__main__":
    df = pandas.read_csv('rishon-letzion.csv')
    print("Raw table: ", df, "\n")

    entitlements,values = get_input_from_raw_table(df.head(10))
    # entitlements,values = get_input_from_raw_table(df)
    print(len(values), " items: ", values, "\n")
    print(len(entitlements), " entitlements: ", entitlements, "\n")
