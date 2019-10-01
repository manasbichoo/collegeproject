import pandas as pd
import sqlite3


conn = sqlite3.connect(r"C:\Users\manas16b\Desktop\COLLEGE PROJECT\example2.db")
cur = conn.cursor()

df=pd.read_sql('select * from Projects where language="HTML"', conn)
conn.commit()
print(df)
conn.close()