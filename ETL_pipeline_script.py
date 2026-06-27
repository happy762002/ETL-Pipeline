import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import os

# Database Connections

engine = create_engine("sqlite:///data.db")
conn = create_engine("mysql+pymysql://root:password@localhost/ecom_db")

# Extract Data

def ingest_db(df, tablename, engine):
    df.to_sql(tablename, con=engine, if_exists='replace', index=False)


def create_sql_file():
    for file in os.listdir("data"):

        if file.endswith(".csv"):

            df = pd.read_csv("data/" + file, encoding="latin1")

            print(df.shape)

            ingest_db(df, file[:-4], engine)

            print(f"{file} Imported Successfully")


def sqlite_to_mysql():

    sqlite_conn = sqlite3.connect("data.db")

    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table';",
        sqlite_conn
    )

    print(tables)

    for table in tables["name"]:

        df = pd.read_sql(
            f"SELECT * FROM `{table}`",
            sqlite_conn
        )

        df.to_sql(
            table,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"{table} imported successfully")

    sqlite_conn.close()

# Transform Data

def check_the_connection():

    print("Connected Successfully")

    df = pd.read_sql_query(
        "SELECT * FROM data LIMIT 10;",
        conn
    )

    print(df)


def datacleaning():

    # global df1

    df1 = pd.read_sql_table(
        table_name="data",
        con=conn
    )

    print(df1.head())

    print("Check The Shape Of the Data\n")
    print(df1.shape)

    print("Check The Datatype Of the Data\n")
    print(df1.dtypes)

    print("Check The Null Values\n")
    print(df1.isnull().sum())

    print("Check The Duplicates\n")
    print(df1.duplicated().sum())

    df1.drop_duplicates(inplace=True)

    print("Duplicates After Drop\n")
    print(df1.duplicated().sum())

    print("Unique CustomerID Count\n")
    print(df1["CustomerID"].value_counts().count())

    print("Unique Description Count\n")
    print(df1["Description"].value_counts().count())

    print("Invoice Count = 1")
    print((df1["InvoiceNo"].value_counts() == 1).sum())

    print("Invoice Count > 1")
    print((df1["InvoiceNo"].value_counts() != 1).sum())

    df1.dropna(subset=["CustomerID"], inplace=True)
    df1.dropna(subset=["Description"], inplace=True)

    return df1

def changing_dtypes(df1):

    # global df1

    print("Datatype Before Conversion\n")
    print(df1.dtypes)

    df1["CustomerID"] = pd.to_numeric(
        df1["CustomerID"],
        errors="coerce"
    )

    df1["UnitPrice"] = pd.to_numeric(
        df1["UnitPrice"],
        errors="coerce"
    )

    df1["InvoiceDate"] = pd.to_datetime(
        df1["InvoiceDate"],
        errors="coerce"
    )

    df1 = df1.astype({
        "UnitPrice": "float",
        "CustomerID": "Int64"
    })

    df1['Quantity'] = pd.to_numeric(df1['Quantity'], errors='coerce')
    
    # convert to positive to negitive
    df1['Quantity'] = df1['Quantity'].abs()

    return df1


def string_manipulating(df1):

    # global df1

    df1 = df1.apply(
        lambda col: col.str.strip()
        if col.dtype == "object"
        else col
    )

    df1["Description"] = (
        df1["Description"]
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    df1.columns = df1.columns.str.strip()

    df1["StockCode"] = (
        df1["StockCode"]
        .str.replace(" ", "")
    )

    return df1

def adding_new_col(df1):
    # add total price
    df1['TotalPrice'] = round(df1['Quantity'] * df1['UnitPrice'],2)
    df1['Year'] = df1['InvoiceDate'].dt.year
    df1['Quarter'] = df1['InvoiceDate'].dt.quarter
    df1['Month'] = df1['InvoiceDate'].dt.month_name()
    df1['Day'] = df1['InvoiceDate'].dt.day_name()
    df1['Weekend'] = df1['Day'].isin(['Saturday','Sunday'])
    df1['Weekend'] = df1['Weekend'].astype('int')
    
    def order_size(qty):
        if qty <= 10:
            return 'Small'
        elif qty <= 50:
            return 'Medium'
        else:
            return 'Large'
    
    df1['OrderSize'] = df1['Quantity'].apply(order_size)

    return df1


def verifying_clean_data(df1):

    # global df1

    print(f"{'-'*50} Verifying Data {'-'*50}")

    print("-"*100)

    print("\nInfo\n")

    df1.info()

    print("\nNull Values\n")
    print(df1.isnull().sum())

    print("\nHead Data\n")
    print(df1.head())

    print("-"*100)

    return df1

# Export

def export(df1):

    # global df1

    df1.to_sql(
        "data_cleaned",
        conn,
        if_exists="replace",
        index=False
    )

    df1.to_csv(
        "data_cleaned.csv",
        index=False
    )

    print("\nData Exported Successfully")

# Main

def main():

    # Extract(From MySQl)
    
    create_sql_file()
    sqlite_to_mysql()

    # Verify Connection 
    check_the_connection()

    # Transform
    df1 = datacleaning()
    df1 = changing_dtypes(df1)
    df1 = string_manipulating(df1)
    df1 = adding_new_col(df1)

    # Verify
    df1 = verifying_clean_data(df1)

    # Load
    export(df1)
    
if __name__ == "__main__":
    main()