import os, sys, gzip, random, csv, json, datetime, re, time
sys.path.append(os.environ['LAV_DIR']+'/src/')
baseDir = os.environ['LAV_DIR']
import pandas as pd
import urllib3, requests
import psycopg2
from sqlalchemy import create_engine

db_name, db_user, db_pass = os.environ['DB_HOST'], os.environ['DB_USER'], os.environ['DB_PASS']
db_host, db_port = os.environ['DB_HOST'], os.environ['DB_USER']

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

res = db.execute("SELECT datname FROM pg_database;")
for r in res: print(r)
res = db.execute("select * from pg_catalog.pg_tables where schemaname = 'public';")
for r in res: print(r)

cred = json.loads(os.environ['CRED_DICT'])['mailreach']
cust_id = 35559

url = cred['url'] + "accounts" # + "?page=0"
resq = requests.get(url,headers=cred['headers'])
print(resq)
resq = resq.json()
l = resq[0].keys()
l1 = [i for i in l if type(resq[0][i]) != dict]
resD = pd.DataFrame.from_dict(resq)
resD.to_csv(baseDir+"/light/raw/mailreach_client.csv",index=False)
resD[l1].to_sql("mailreach",db,if_exists="replace")


url = "http://localhost:8010" + "/product/1" # + "?page=0"
resq = requests.get(url)
print(resq.json())
prod = {"name":"test product", "price": 11.22}



baseUrl = cred['url'] + "accounts/" + str(cust_id)
resq = requests.post(url,headers=cred['headers'],params=cred['params']).json()
resD = pd.DataFrame.from_dict([l1])
resD.to_csv(baseDir+"/light/raw/mailreach.csv",index=False)




Main account Customer ID = 2402
[https://app.mailreach.co/dashboard/2402/account/](https://app.mailreach.co/dashboard/2402/account/)
[https://app.mailreach.co/dashboard/2402/accounts/23545/show](https://app.mailreach.co/dashboard/2402/accounts/23545/show)
[https://mailreach-api.readme.io/password?redirect=/](https://mailreach-api.readme.io/password?redirect=/)
[https://mailreach-api.readme.io/](https://mailreach-api.readme.io/)


## Project Idea
Get all mailboxes and have a DB→Table MailreachAccounts
Get mailboxes ID and import where all messages arrived (like example below)
The table should be like:
MailboxId,Mailbox,Date,LandedInbox,LandedSpam,LandedCategories,Missing,
Provider = Gmail,MS,Others

Ideas of what to do with the info:

- CLIENT UI
- Display warming data for clients, possibly % of spam placement = Landed in Spam vs Sent
- OPERATIONS:
- Create triggers / emails for Ops or later for clients when something goes out of normal meaning something happen meaning reputation of domain was damaged because more emails are landing in spam FI
- INTERNAL STUDIES:
- Co-relate warming data with Google Postmaster = Domain reputation
    - Domain reputation changes impact warming inbox placament data?
    - 
- Co-relate warming data with Sending Data = % of bounces /
    - % of bounce changes (decrease or increase) impact

## Important Functions
Create an account
[https://mailreach-api.readme.io/reference/postv1imapauth](https://mailreach-api.readme.io/reference/postv1imapauth)
POST [https://api.mailreach.co/api/v1/imap_auth](https://api.mailreach.co/api/v1/imap_auth)
## CURL commands from Cesar

Create/Update a mailbox Example

```python
curl --request POST -H 'X-Api-Key:Bearer KCVPTrGomAfKmsTwe6A5hkx5' --header 'Content-Type: application/x-www-form-urlencoded' --url 'https://api.mailreach.co/api/v1/imap_auth' --data-urlencode 'email=mo@mymarketerhire.com' --data-urlencode 'password=YIkSlBDeo4PQKMLH/yPFJ2D6CqYK5e4r' --data-urlencode 'first_name=Mo' --data-urlencode 'last_name=Hassoun' --data-urlencode 'imap_server=mail.lightmetermail.io' --data-urlencode 'imap_server_port=993' --data-urlencode 'imap_server_username=mo@mymarketerhire.com' --data-urlencode 'imap_server_password=YIkSlBDeo4PQKMLH/yPFJ2D6CqYK5e4r' --data-urlencode 'smtp_server=mail.lightmetermail.io' --data-urlencode 'smtp_server_username=mo@mymarketerhire.com' --data-urlencode 'smtp_server_password=YIkSlBDeo4PQKMLH/yPFJ2D6CqYK5e4r' --data-urlencode 'smtp_server_port=587' --data-urlencode 'smtp_server_auth_type=login' --data-urlencode 'smtp_server_starttls=true' --data-urlencode 'provider=custom'
```

Update mailbox ramp-up

```python
curl --request POST -H 'X-Api-Key:Bearer KCVPTrGomAfKmsTwe6A5hkx5' --header 'Content-Type: application/x-www-form-urlencoded' --url 'https://api.mailreach.co/api/v1/accounts/35559' --data-urlencode config_rampup_target=25 --data-urlencode config_rampup_increase=2
```
