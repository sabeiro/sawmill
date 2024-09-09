import json, random, datetime, time, sys, re, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import sqlite3
from sqlite3 import Error
import numpy as np
from bs4 import BeautifulSoup

baseDir = "/home/pi/bottino/" 
os.environ['PATH'] = os.environ['PATH'] + ":" + baseDir + "src/"
os.environ['DISPLAY'] = ":10"

DATE_FORMAT = "%Y_%m_%d"
raw = pd.read_csv(baseDir + "Production_poi.csv")
con = sqlite3.connect(baseDir + "location_metadata.db")          #Path to SQL Database
date = datetime.datetime.now().strftime(DATE_FORMAT)


from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = False
binary = FirefoxBinary('/usr/bin/firefox')
browser = webdriver.Firefox(capabilities=cap,executable_path=baseDir+"geckodriver",firefox_binary=binary,options=options)

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('/usr/bin/firefox')
options = Options()
options.headless = True
options.add_argument("disable-infobars")
options.add_argument("--mute-audio")
options.add_argument("--lang=de")
options.add_argument("--headless")
profile = webdriver.FirefoxProfile()
geckopath = baseDir+"geckodriver"
browser = selenium.webdriver.Firefox(capabilities=DesiredCapabilities.FIREFOX,executable_path=geckopath,firefox_profile=profile,firefox_binary=binary,options=options)
browser.get("http://google.com")


from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=os.path.abspath("bottino/chromedriver"),chrome_options=options)

options = Options()
options.add_argument("disable-infobars")
options.add_argument("--mute-audio")
options.add_argument("--lang=de")
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=baseDir+"chromedriver",options=options)


df = pd.read_csv(baseDir + "log/statWeek/actRep/dom_h.csv.gz",compression="gzip")

print("-----------Update Database at "+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" ----------")
i = 0
for index,data in raw.iterrows():
    print(str(i)+") Get website from url for "+str(data["id_poi"]))
    try:
        driver.get(str(data["url"]))
    except:
        print(str(i)+") No website found for "+str(data["id_poi"])+". Skip Location.")
        continue
    driver.implicitly_wait(random.randint(10,60))
    
    print(str(i)+") Read html data from website for "+str(data["id_poi"]))
    html_string = str(BeautifulSoup(driver.page_source, 'html.parser'))
    
    print(str(i)+") Find livedata for visitors "+str(data["id_poi"]))
    Live_Data = re.findall(r"class=\"lubh-bar lubh-sel(.*?)\">", html_string)
    Live_Data = re.findall(r"height:(.*?)px", str(Live_Data))
    Unix_Timestamp = int(time.time())
    
    print(str(i)+") Update database "+str(data["id_poi"]))
    with con:
            cur = con.cursor()
            con.row_factory = sqlite3.Row
            if True:
                cur.execute("INSERT INTO TuR_Livedata"        
                        "("
                        "id_poi,"
                        "timestamp,"
                        "value,"
                        "url"
                      ") VALUES (?,?,?,?)",
                (
                    str(data["id_poi"]),
                    str(Unix_Timestamp),
                    str(Live_Data[0]),
                    str(data["url"]),
                )
            )

    print(str(i)+") Data gathered for: "+str(data["id_poi"])+" at "+datetime.datetime.utcfromtimestamp(Unix_Timestamp).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
    i = i+1
    driver.implicitly_wait(random.randint(10,60))
    driver.close()
print("---------------------------------------------------Database updated------------------------------------------------------------------")

if False:
    driver.close()




options = Options()
options.add_argument("disable-infobars")
options.add_argument("--mute-audio")
options.add_argument("--lang=de")
driver = webdriver.Chrome(executable_path=chrome_driver_path,options=options)
print(str(i)+") Get website from url for "+str(data["id_poi"]))
try:
    driver.get(str(data["url"]))
except:
    print(str(i)+") No website found for "+str(data["id_poi"])+". Skip Location.")
driver.implicitly_wait(random.randint(10,60))

print(str(i)+") Read html data from website for "+str(data["id_poi"]))
html_string = str(BeautifulSoup(driver.page_source, 'html.parser'))

print(str(i)+") Find livedata for visitors "+str(data["id_poi"]))
Live_Data = re.findall(r"class=\"lubh-bar lubh-sel(.*?)\">", html_string)
Live_Data = re.findall(r"height:(.*?)px", str(Live_Data))
Unix_Timestamp = int(time.time())
    
print(str(i)+") Update database "+str(data["id_poi"]))
with con:
    cur = con.cursor()
    con.row_factory = sqlite3.Row
    if True:
        cur.execute("INSERT INTO TuR_Livedata"        
                    "("
                    "id_poi,"
                    "timestamp,"
                    "value,"
                    "url"
                    ") VALUES (?,?,?,?)",
                    (
                        str(data["id_poi"]),
                        str(Unix_Timestamp),
                        str(Live_Data[0]),
                        str(data["url"]),
                    )
        )

print(str(i)+") Data gathered for: "+str(data["id_poi"])+" at "+datetime.datetime.utcfromtimestamp(Unix_Timestamp).strftime('%Y-%m-%d %H:%M:%S')+" UTC")
i = i+1
driver.implicitly_wait(random.randint(10,60))
driver.close()

    
