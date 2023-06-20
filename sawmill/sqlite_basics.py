import pandas as pd
import sqlite3
import jaydebeapi
import pandas as pd
import numpy as np
database = "/home/sabeiro/tmp/light/bounces.db"

import sqlite3 as lite
import sys 
con = lite.connect(database)
cur = con.cursor()
query = "SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY 1;"
print(cur.execute(query))

query = "SELECT * from recipients;" # bounced
bouncedD = pd.read_sql_query(query,con)
query = "SELECT * from spammed;" # spammed emails
spamD = pd.read_sql_query(query,con)
# all sent messages (category: apollo [prospecting mail client]) 
sentD = pd.read_csv("/home/sabeiro/tmp/light/query_res.csv") 

statusD = pd.merge(sentD,bouncedD,how="left",left_on="mail_to",right_on="email")
statusD.loc[:,"bounced"] = statusD["comment"].apply(lambda x: x == x)
statusD.loc[:,"day"] = statusD["datetime"].apply(lambda x: x[:10])
statusD.loc[:,"sent"] = statusD["datetime"].apply(lambda x: 1)
print(np.sum(statusD["bounced"])/statusD.shape[0])
statusG = statusD.groupby("day").sum()
