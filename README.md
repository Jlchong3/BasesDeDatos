# Database Management Script README

## Overview

This Python script provides a command-line interface for managing records in a MySQL database hosted on Azure. The script enables users to perform various operations such as adding, deleting, and editing records, as well as querying data. It uses the `pandas` library for tabular display and the `mysql-connector` library for database connectivity.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python (version 3.x)
- pandas library (`pip install pandas`)
- mysql-connector library (`pip install mysql-connector-python`)

## Configuration

Update the database connection details in the script:

```python
conn = sql.connect(
    host = "basesloteria.mysql.database.azure.com",
    user = "administrador",
    password = "@basesloteriaN",
    database = "loterianacional",
    autocommit=True
)
```

## Usage

1. Run the script in a Python environment:

   ```bash
   python script.py
   ```

2. The script will display the available tables in the connected database.

3. Choose an option from the menu (1 to 5) to perform the desired operation:

   - **Option 1: Add Record**
     - Allows users to add a new record to a selected table.

   - **Option 2: Delete Record**
     - Enables users to delete a record from a selected table. The script prompts for the values of the primary key columns.

   - **Option 3: Edit Record**
     - Lets users edit an existing record in a selected table. Users are prompted to enter new values for each column.

   - **Option 4: Query Record**
     - Performs a simple query on a selected table based on a provided primary key value.

   - **Option 5: Exit**
     - Terminates the script.

## Additional Information

- The script uses exception handling to address errors during database operations.

- The `pandas` library is employed to display table content in a tabular format.

- The script ensures proper closure of the database cursor.

## Note

- Make sure to back up your database before performing operations that modify data.

- Review and update the script according to your database schema and requirements.

Feel free to contact the script author for any questions or issues.
