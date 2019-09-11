import pandas as pd
import sqlite3


conn = sqlite3.connect(r"C:\Users\manas16b\Desktop\COLLEGE PROJECT\example.db")
cur = conn.cursor()

df=pd.read_sql('select * from Projects', conn)
conn.commit()
print(df)
conn.close()