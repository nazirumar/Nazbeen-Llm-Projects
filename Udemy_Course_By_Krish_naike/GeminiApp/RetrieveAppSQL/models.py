import sqlite3
import os 
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(os.path.join('RetrieveApp/', 'student.db'))

cursor=conn.cursor()

## create the table
table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);

"""
cursor.execute(table_info)

cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Sudhanshu','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Darius','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Vikash','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')
# Commit the transaction
conn.commit()

# Query to verify the insertion
cursor.execute('SELECT * FROM student')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
