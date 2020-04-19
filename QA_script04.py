# import all the needed modules
import pandas as pd
import os
import itertools
import collections
count = collections.Counter()

#-------------------------------------------------------------------------------
""" Products that are most often sold together """
#-------------------------------------------------------------------------------


### Start : Collect All Data at one place --------------------------------------
df_allmonthsdata = pd.DataFrame()
listfile = os.listdir('Sales_Data')
print("Name of Files available in folder : ", ", ".join(listfile))
print("Total count of files : ", len(listfile))

for csvf in listfile:
    dfsalesdt = pd.read_csv('Sales_Data/' + csvf)  # Read CSVs of the folder one by one
    df_allmonthsdata = pd.concat([df_allmonthsdata, dfsalesdt])  # Concatenate the data of CSV's into dataframe

print("Length of new Dataframe which has 12 month's data : ", len(df_allmonthsdata))
df_allmonthsdata.to_csv("Output/alldata.csv", index=False)
# here index=False does not include index i.e. 0,1,2,3......
# here index=True includes index i.e. 0,1,2,3......

df_allmonthsdata = pd.read_csv("Output/alldata.csv") # Read CSV to start Fresh
### End : Collect All Data at one place ---------------------------------------


### Start : Clean up the Data -------------------------------------------------
#### Check NaN values present
nan_val = df_allmonthsdata[df_allmonthsdata.isna().any(axis=1)]
print("Check NaN values present : ",nan_val.head())
#### Drop rows of NAN
df_allmonthsdata = df_allmonthsdata.dropna(how="all")
invalid_data = df_allmonthsdata[df_allmonthsdata["Order Date"].str[0:2] == 'Or']
print("Invalid values present : ", invalid_data.head())
# Now Select Correct Data which does not have "Or" value in Date
df_allmonthsdata = df_allmonthsdata[df_allmonthsdata["Order Date"].str[0:2] != 'Or']

#### Convert Columns to appropriate data type
df_allmonthsdata["Quantity Ordered"] = pd.to_numeric(df_allmonthsdata["Quantity Ordered"]) # Make int
df_allmonthsdata["Price Each"] = pd.to_numeric(df_allmonthsdata["Price Each"]) # Make int
### End : Clean up the Data -------------------------------------------------


### Start : find Order id which is present more than once, i.e. more than one product under same order----------------------------
needed_data = df_allmonthsdata[df_allmonthsdata["Order ID"].duplicated(keep=False)]
print("Retrieve & Collect only Duplicate : ",needed_data.head())
needed_data["list_of_products"] = needed_data.groupby("Order ID")["Product"].transform(lambda x: ','.join(x))
# Meaning of above line is, make a group of Products separated by comma and store in new Column, on the basis of similar Order IDs
print("Check list_of_products Column & All Data : ",needed_data.head())
# Above line shows Same order id more than once which is correct but we want all duplicates lines should be combined together
needed_data = needed_data[['Order ID','list_of_products']].drop_duplicates()
# Above will create DataFrame of two columns 'Order ID','list_of_products' with combined manner.
print("Show only one record, removed duplicates : ",needed_data.head())
sort_data = needed_data.sort_values(by=["list_of_products"])
print("Sorted Data : ",sort_data.head())
### End : find Order id which is present more than once, i.e. more than one product under same order----------------------------


### Start : find pair of products which is present more than once----------------------------
for row in sort_data["list_of_products"]:
    row_list = row.split(",")
    count.update(collections.Counter(itertools.combinations(row_list,2)))
    # In above, 2 is count of products order together
    # we can try with 3 as well, but output with 2 is accurate as compare to 3 or 4....
print("Products and its count : ",count.most_common(1)) # here 1 is 1st value = (('iPhone', 'Lightning Charging Cable'), 1005)
""" Answer : products that are most often sold together are : 'iPhone', 'Lightning Charging Cable' , both order 1005 times together """
### End : find pair of products which is present more than once----------------------------

#-------------------------------------------------------------------------------
""" End of : Products that are most often sold together """
#-------------------------------------------------------------------------------