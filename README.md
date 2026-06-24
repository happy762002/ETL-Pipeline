-------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ETL-Pipeline (E-commerce Sales)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
### <u>`Architecture`</u>

MySQL Database<br>
      │<br>
      ▼<br>
Python ETL Script<br>
(Extract → Transform → Load)<br>
      │<br>
      ▼<br>
Cleaned Data Warehouse<br>
(CSV / Excel / PostgreSQL)<br>
      │<br>
      ▼<br>
Power BI / Tableau Dashboard<br>
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
### The Steps 1 Performed

#### Day 1 (ETL Process)

* Established a connection with SQLite and created the `data.db` database file.
* Imported the CSV data into the database with the table name `data`.
* To avoid errors while importing the data into MySQL, I converted all column datatypes to `TEXT`.
* After that, I exported (dumped) the SQLite database for migration to MySQL Server.
* Created a Python script to import the data from SQLite to MySQL for further analysis.

**Note:**

* In this case, the dataset contained values that did not match the expected datatypes. Therefore, I converted all columns to the `TEXT` datatype before migration.
* If the dataset already follows the target table schema and datatypes, it can be imported directly into MySQL without using a Python migration script.
