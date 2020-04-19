# import all the needed modules
import pandas as pd
import os
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------------
""" At What time we should show advertisements so Customer will have attention to it,
 and maximum the chance of buying products  """
# -------------------------------------------------------------------------------


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
df_allmonthsdata = pd.read_csv("Output/alldata.csv")  # Read CSV to start Fresh
### End : Collect All Data at one place ---------------------------------------


### Start : Clean up the Data -------------------------------------------------
#### Check NaN values present
nan_val = df_allmonthsdata[df_allmonthsdata.isna().any(axis=1)]
print("Check NaN values present : ", nan_val.head())
#### Drop rows of NAN
df_allmonthsdata = df_allmonthsdata.dropna(how="all")
invalid_data = df_allmonthsdata[df_allmonthsdata["Order Date"].str[0:2] == 'Or']
print("Invalid values present : ", invalid_data.head())
# Now Select Correct Data which does not have "Or" value in Date
df_allmonthsdata = df_allmonthsdata[df_allmonthsdata["Order Date"].str[0:2] != 'Or']
#### Convert Columns to appropriate data type
df_allmonthsdata["Quantity Ordered"] = pd.to_numeric(df_allmonthsdata["Quantity Ordered"])  # Make int
df_allmonthsdata["Price Each"] = pd.to_numeric(df_allmonthsdata["Price Each"])  # Make int
#### Remove unnecessary Column if any, currently there is no, but below is just to have an idea
# df_allmonthsdata.drop(columns="Price",inplace=True) # 1st way
# df_allmonthsdata = df_allmonthsdata.drop(columns="Price") # 2nd way
### End : Clean up the Data -------------------------------------------------


### Start : find hour & minute on the basis of Order Date Column ----------------------------
# 1st way - Time Consuming
# df_allmonthsdata["Order_date_dt"] = pd.to_datetime(df_allmonthsdata["Order Date"])
# In Above : Convert data type to datetime from Series
# df_allmonthsdata["hour"] = df_allmonthsdata["Order_date_dt"].dt.hour
# df_allmonthsdata["minute"] = df_allmonthsdata["Order_date_dt"].dt.minute
# print(df_allmonthsdata.head())
# 2nd way -
df_allmonthsdata["hour"] = df_allmonthsdata["Order Date"].apply(lambda x: x.split(" ")[1][:2])
df_allmonthsdata["minute"] = df_allmonthsdata["Order Date"].apply(lambda x: x.split(" ")[1][3:])
print("Added new Hour and Minute Columns : ",df_allmonthsdata.head())
### End : find hour & minute on the basis of Order Date Column ----------------------------

### Start : Actual Answer : Best hours ----------------------------------------------------
hours = [i[0] for i in df_allmonthsdata.groupby('hour')]  # X Axis - Hours
products = [i[1]["Product"].count() for i in df_allmonthsdata.groupby('hour')]  # Y Axis - Products count
best_hrs = df_allmonthsdata.groupby('hour').count()
print("All Data with Count : ",best_hrs)
print("X-Axis Hours : ",hours)
print("Y-Axis Orders : ",products)
""" Answer : Best Hours recommendation is around 11AM and 7PM as per graph"""
### End : Actual Answer : Best hours -------------------------------------------------------

### Start : Show Actual Answer on Graph : Find Best City had highest number of sales -------------
plt.plot(hours, products)
# plt.bar(hours,products)
plt.xticks(hours)  # Show each city on X Axis & size is Font Size
plt.grid()  # Lines on a graph
plt.ylabel("Orders Count")
plt.xlabel("Hours")
plt.show()
### End : Show Actual Answer on Plot : Find Best City had highest number of sales ---------------


# -------------------------------------------------------------------------------
""" At What time we should show advertisements so Customer will have attention to it,
 and maximize the chance of buying products  """
# -------------------------------------------------------------------------------