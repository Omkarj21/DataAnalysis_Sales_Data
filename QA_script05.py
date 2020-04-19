# import all the needed modules
import pandas as pd
import os
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
""" Which products sold most and why """
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


### Start : Calculate products sold most on the basis of Quantity Ordered and Its Price----------------------------
product_group = df_allmonthsdata.groupby("Product")
qty_ordered = product_group.sum()["Quantity Ordered"]
products = [product for product,df in product_group]
print(products)
prices = df_allmonthsdata.groupby("Product").mean()["Price Each"]
print(prices)
### End : Calculate products sold most on the basis of Quantity Ordered and Its Price----------------------------


### Start : Show Actual Answer on Plot : Find products sold most on the basis of Quantity Ordered and Its Price -------------
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products,qty_ordered,color="g")
ax2.plot(products,prices,"b-")
ax1.set_xlabel("Product Name")
ax1.set_ylabel("Quantity Ordered", color="g")
ax2.set_ylabel("Price ($)",color="b")
ax1.set_xticklabels(products,rotation="vertical",size=8)
plt.show()
### End : Show Actual Answer on Plot : Find products sold most on the basis of Quantity Ordered and Its Price ---------------


#-------------------------------------------------------------------------------
""" End of : Which products sold most and why """
#-------------------------------------------------------------------------------