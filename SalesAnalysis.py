import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
from collections import Counter
all_data = pd.read_csv(r"C:\Users\aditya gaur\OneDrive\Desktop\seminar\SalesAnalysis\Output\all_data.csv")


# cleaning data
nan_df = all_data[all_data.isna().any(axis=1)] # deleting all NaN values
all_data = all_data.dropna(how="all")
all_data = all_data[all_data['Order Date'].str[0:2] != "Or"] # removing all the duplicated columns
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data["Price Each"] = pd.to_numeric(all_data["Price Each"])


# augumenting data with additional columns
all_data["Month"] = all_data["Order Date"].str[0:2] # add month columns
all_data["Month"] = all_data["Month"].astype('int32')
all_data["Sales"] = all_data["Quantity Ordered"] * all_data["Price Each"] # adding the sales columns


def get_city(address):
 return address.split(",")[1]


def get_state(address):
 return address.split(',')[2].split(" ")[1]


all_data["City"] = all_data['Purchase Address'].apply(lambda x: get_city(x) + " ( "
+ get_state(x) + " ) ")


# finding best month for sales and earning that month
sales = all_data.groupby("Month").sum()
months = range(1, 13)
plt.bar(months, sales['Sales'])
plt.xticks(months)
plt.ylabel("Sales in USD")
plt.xlabel("Months")
plt.show()


# what US city had the highest number of sales
results = all_data.groupby("City").sum()
cities = [city for city, df in all_data.groupby("City")]
plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation="vertical", size = 6)
plt.ylabel("Sales in USD")
plt.xlabel("City names")
plt.show()


# what time we should display our advertisement to maximize viewership
all_data["Order Data"] = pd.to_datetime(all_data["Order Date"])
all_data["Hour"] = all_data["Order Data"].dt.hour
all_data["Minute"] = all_data["Order Data"].dt.minute
hours = [hour for hour,all_data in all_data.groupby("Hour")]
plt.plot(hours, all_data.groupby(["Hour"]).count())
plt.xticks(hours)
plt.xlabel("hour")
plt.ylabel("Number of orders")
plt.grid()
plt.show()


# what products are most often sold together
df1 = all_data[all_data["Order ID"].duplicated(keep=False)]
df1["Grouped"] = df1.groupby("Order ID")["Product"].transform(lambda x:
",".join(x))
df1 = df1[["Order ID", "Grouped"]].drop_duplicates()
count = Counter()
for row in df1["Grouped"]:
 row_list = row.split(",")
 count.update((Counter(combinations(row_list,2))))
for key, value in count.most_common(10):
 print(key,value)


# find the product which is sold the most
product_group = all_data.groupby("Product")
quantity_ordered = product_group.sum()['Quantity Ordered']
products = [product for product, df in product_group]
plt.bar(products, quantity_ordered)
plt.xlabel("Products")
plt.ylabel("Quantity Ordered")
plt.xticks(products, rotation = "vertical", size=6)


# overlaying secondary y-axis for price correlation
prices = all_data.groupby("Product").mean()["Price Each"]
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, "b-")
ax1.set_xlabel("Product Name")
ax1.set_ylabel("Quantity Ordered", color="g")
ax2.set_ylabel("Prices in USD", color='b')
ax1.set_xticklabels(products, rotation="vertical", size=6)
plt.show()