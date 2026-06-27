import pandas as pd

# Read Excel file
df = pd.read_excel("Customer Call List.xlsx")

# Remove duplicate rows
df = df.drop_duplicates()

# Drop unwanted column
df = df.drop(columns="Not_Useful_Column", errors="ignore")

# Clean Last_Name column
df["Last_Name"] = df["Last_Name"].str.strip("123._/")

# Clean Phone_Number
df["Phone_Number"] = (
    df["Phone_Number"]
    .astype(str)
    .str.replace(r"[^0-9]", "", regex=True)
    .str.replace(r"(\d{3})(\d{3})(\d{4})", r"\1-\2-\3", regex=True)
)

# Split Address into new columns
address = df["Address"].str.split(",", n=2, expand=True)
df["Street_Address"] = address[0]
df["State"] = address[1]
df["Zip_Code"] = address[2]

# Replace Y/N in Paying Customer
df["Paying Customer"] = df["Paying Customer"].replace({
    "Y": "Yes",
    "N": "No",
    "N/a": ""
}).fillna("")

# Replace Y/N in Do_Not_Contact
df["Do_Not_Contact"] = df["Do_Not_Contact"].replace({
    "Y": "Yes",
    "N": "No",
    "N/a": ""
}).fillna("")

# Remove rows where Do_Not_Contact is Yes
df = df[df["Do_Not_Contact"] != "Yes"]

# Remove rows with no phone number
df = df[df["Phone_Number"] != ""]
df = df[df["Phone_Number"] != "nan"]

# Display final cleaned data
print(df)
print("===== DATA CLEANING REPORT =====")
print("Total Records:", len(df))
print("Total Columns:", len(df.columns))

print("\nPaying Customer:")
print(df["Paying Customer"].value_counts())

print("\nDo Not Contact:")
print(df["Do_Not_Contact"].value_counts())


report = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Total Columns",
        "Paying Customers",
        "Do Not Contact Customers"
    ],
    "Value": [
        len(df),
        len(df.columns),
        (df["Paying Customer"] == "Yes").sum(),
        (df["Do_Not_Contact"] == "Yes").sum()
    ]
})

report.to_excel("Data_Cleaning_Report.xlsx", index=False)