# import all the needed modules
import pandas as pd
import os
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
"""Find Best Month sales and How much earned into that month"""
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


### Start : find month number & add new month Column ----------------------------
# We would need to find month and we have date thru which we can find month number
# 1st way to find Month Number
# df_allmonthsdata["month"] = df_allmonthsdata["Order Date"][0][:str(df_allmonthsdata["Order Date"][0]).find("/")]
# 2nd way to find Month Number
df_allmonthsdata["month"] = df_allmonthsdata["Order Date"].str[0:2] # Month will be "04"
df_allmonthsdata["month"] = df_allmonthsdata["month"].astype('int32') # Month will be "4"
print(df_allmonthsdata.head())
# df_allmonthsdata["month"] = pd.to_numeric(df_allmonthsdata["month"])
# df_allmonthsdata.astype({"month": 'int32'}).dtypes()
print(type(df_allmonthsdata["month"]))
### End : find month number & add new month Column -----------------------------


### Start : Calculate Sales & add Sales new month Column ----------------------------
df_allmonthsdata["Sales"] = df_allmonthsdata["Quantity Ordered"] * df_allmonthsdata["Price Each"]
print(df_allmonthsdata["Sales"])
### End : Calculate Sales & add Sales new month Column ------------------------------


### Start : Actual Answer : Find Best Month sales and How much earned into that month -------------
best_sale_month_data = df_allmonthsdata.groupby('month').sum()
print(best_sale_month_data)
# print(df_allmonthsdata.groupby('month').sum())
# print(df_allmonthsdata.groupby('month').sum()["Sales"]) # To See only Sales Column
""" Answer : Best Month is 12th month i.e. December having Sales 4.613443e+06 $ """
### End : Actual Answer : Find Best Month sales and How much earned into that month ---------------


### Start : Show Actual Answer on Plot : Find Best Month sales and How much earned into that month -------------
months = range(1,13) # X Axis month : 13 is exclusive, i.e it will show from 1 to 12 month
plt.bar(months,best_sale_month_data["Sales"])
plt.xticks(months) # Show each month on X Axis
plt.ylabel("Sales in USD $")
plt.xlabel("Month Number")
plt.show()
### End : Show Actual Answer on Plot : Find Best Month sales and How much earned into that month ---------------


#-------------------------------------------------------------------------------
""" End of : Find Best Month sales and How much earned into that month """
#-------------------------------------------------------------------------------