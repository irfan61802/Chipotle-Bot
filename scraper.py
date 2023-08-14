import time
import os
import re
import ppadb

from ppadb.client import Client
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


adb = Client(host='localhost', port=5037)
devices = adb.devices()
devList=[str(d.serial) for d in devices]

# url of the page we want to scrape
url = "https://www.twitter.com/chipotletweets"

# block images to increase speed
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
driver.get(url) 

currentCode=""
count=0

while True:
    # start_time = time.perf_counter()
    driver.refresh()
    time.sleep(1) 
    #WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, "article")))

    html = driver.page_source
    # apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")

    # get all text off in span tag
    page = soup.find_all('span')
    for p in page:
        t=p.getText()
        if "Text" in t or "text" in t:
            codeArr=t.split()
            if "Text" in t:
                codeIndex=codeArr.index("Text")+1
            elif "text" in t:
                codeIndex=codeArr.index("text")+1

            if currentCode!=re.escape(codeArr[codeIndex]):
                currentCode=re.escape(codeArr[codeIndex])
                for d in devList:
                    os.system('platform-tools\\adb.exe -s '+d+' shell am startservice --user 0 -n com.android.shellms/.sendSMS -e contact 888222 -e msg \"'+currentCode+'\"') 

            print(count,": "+currentCode)
            count+=1
            break
    # if count==50:
    #     end_time = time.perf_counter()
    #     print(end_time - start_time)
    #     break
    

driver.close() # closing the webdriver