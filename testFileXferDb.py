import sqlite3
from datetime import datetime, timedelta

sqlite_file = 'fileXferTimeData.sqlite'    # name of the sqlite database file
table_name = 'date_time_file_transfer'   # name of the table to be created
index_name = 'unique_index' # index names
main_column = 'last_check_column' # name of the PRIMARY KEY column
column_type = 'TEXT' # E.g., INTEGER, TEXT, NULL, REAL, BLOB, (TEXT REAL or INTEGER for Date and Time)
default_val = '19:31:47.282902' # a default value for the new column rows



def updateTime():
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute("INSERT INTO date_time_file_transfer (last_check_column) VALUES (?)", (str(datetime.now()),))

    c.execute("SELECT last_check_column FROM date_time_file_transfer WHERE unique_index = (SELECT MAX(unique_index) FROM date_time_file_transfer)")
    print(c.fetchone())


##SELECT * FROM TABLE WHERE ID = (SELECT MAX(ID) FROM TABLE);

    conn.commit()
    conn.close()

updateTime()    

