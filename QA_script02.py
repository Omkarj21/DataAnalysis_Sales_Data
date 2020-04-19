# import all the needed modules
import pandas as pd
import os
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
""" Find Best City had highest number of sales """
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
#### Remove unnecessary Column if any, currently there is no, but below is just to have an idea
# df_allmonthsdata.drop(columns="Price",inplace=True) # 1st way
# df_allmonthsdata = df_allmonthsdata.drop(columns="Price") # 2nd way
### End : Clean up the Data -------------------------------------------------


### Start : Calculate Sales & add new Sales Column ----------------------------
df_allmonthsdata["Sales"] = df_allmonthsdata["Quantity Ordered"] * df_allmonthsdata["Price Each"]
print(df_allmonthsdata["Sales"])
### End : Calculate Sales & add new Sales Column -------------------------------


### Start : Calculate Sales in City & add new City Column ----------------------------
# 1st way =>
df_allmonthsdata["City"] = df_allmonthsdata["Purchase Address"].apply(lambda x: x.split(",")[1] + "(" + x.split(",")[2][1:3] +")")
print(df_allmonthsdata["City"].head())
# AND (Use any one)
# 2nd way =>
# def get_city(address):
#     return address.split(",")[1]
# def get_state(address):
#     return address.split(",")[2][1:3]
# df_allmonthsdata["City"] = df_allmonthsdata["Purchase Address"].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
# print(df_allmonthsdata["City"].head())
### End : Calculate Sales in City & add new City Column ------------------------------


### Start : Actual Answer : Find Best City had highest number of sales -------------
# best_sale_city_data = df_allmonthsdata.groupby('City').sum().sort_values(by='Sales', ascending=False)
best_sale_city_data = df_allmonthsdata.groupby('City').sum()
print(best_sale_city_data)
# print(df_allmonthsdata.groupby('month').sum())
# print(df_allmonthsdata.groupby('month').sum()["Sales"]) # To See only Sales Column
""" Answer : Best City is San Francisco(CA) having Sales 8.262204e+06 $ """
### End : Actual Answer : Find Best City had highest number of sales ---------------


### Start : Show Actual Answer on Graph : Find Best City had highest number of sales -------------
cities = [i[0] for i in df_allmonthsdata.groupby('City')] # X Axis - Unique City names
sales = [i[1]["Sales"].sum() for i in df_allmonthsdata.groupby('City')] # Y Axis - Total Sales
print(cities)
print(sales)
plt.bar(cities,sales)
plt.xticks(cities,rotation="vertical",size=8) # Show each city on X Axis & size is Font Size
plt.ylabel("Sales in USD $")
plt.xlabel("City Name")
plt.show()
### End : Show Actual Answer on Plot : Find Best City had highest number of sales ---------------


#-------------------------------------------------------------------------------
""" End of : Find Best City had highest number of sales """
#-------------------------------------------------------------------------------