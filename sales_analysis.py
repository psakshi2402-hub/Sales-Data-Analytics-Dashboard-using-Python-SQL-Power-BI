import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# -----------------------------
# STEP 1: CREATE DATASET
# -----------------------------

np.random.seed(42)
n = 10000

data = pd.DataFrame({
    "Order_ID": np.arange(1, n+1),
    "Order_Date": pd.date_range(start="2023-01-01", periods=n, freq='h'),
    "Region": np.random.choice(["North", "South", "East", "West"], n),
    "Product_Category": np.random.choice(["Electronics", "Clothing", "Furniture"], n),
    "Product_Name": np.random.choice(["Laptop", "Shirt", "Table", "Mobile", "Sofa"], n),
    "Quantity": np.random.randint(1, 5, n),
    "Price": np.random.randint(500, 5000, n)
})

data["Total_Sales"] = data["Quantity"] * data["Price"]

data.to_csv("sales_dataset.csv", index=False)
print("Dataset Created Successfully!")

# -----------------------------
# STEP 2: DATA CLEANING
# -----------------------------

df = pd.read_csv("sales_dataset.csv")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Month"] = df["Order_Date"].dt.month
df["Year"] = df["Order_Date"].dt.year

print("\nTotal Revenue:", df["Total_Sales"].sum())

# -----------------------------
# STEP 3: EDA
# -----------------------------

region_sales = df.groupby("Region")["Total_Sales"].sum()
monthly_sales = df.groupby("Month")["Total_Sales"].sum()

print("\nSales by Region:")
print(region_sales)

print("\nMonthly Sales:")
print(monthly_sales)

# -----------------------------
# STEP 4: VISUALIZATION
# -----------------------------

plt.figure()
region_sales.plot(kind='bar')
plt.title("Sales by Region")
plt.ylabel("Revenue")
plt.show()

plt.figure()
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.ylabel("Revenue")
plt.show()

# -----------------------------
# STEP 5: SQL ANALYSIS
# -----------------------------

conn = sqlite3.connect("sales.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

query = """
SELECT Product_Name, SUM(Total_Sales) as Revenue
FROM sales
GROUP BY Product_Name
ORDER BY Revenue DESC
LIMIT 5
"""

top_products = pd.read_sql(query, conn)

print("\nTop 5 Products by Revenue:")
print(top_products)

conn.close()