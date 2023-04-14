# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import datetime
import requests
import csv
import string
import json
from fake_useragent import UserAgent
import openpyxl

# Time to wait for SELECTORS.(second)
WAIT = 4

def get_selectors(text):

    SELECTORS = []
    for font_size in range(1,7):
        font_size = str(font_size)
        selectors = [
            f'//*[preceding-sibling::h{font_size}[1]="{text}" and following-sibling::h{font_size}[1]]',
            # f'//*[. ="{text}"]/ancestor-or-self::h{font_size}/following-sibling::*'
        ]
        SELECTORS += selectors

    print(SELECTORS)
    return SELECTORS

def click_selectors(text):
    SELECTORS = [f'//*[. ="{text}"]']

    return SELECTORS

FIELDNAMES = ['NAME','KEYWORD', 'CONTENT']

# This method is for chrome driver initialization. You can customize if you want.
def setDriver():
    seleniumwire_options = {}
    seleniumwire_options['exclude_hosts'] = ['google-analytics.com']

    # Secure Connection

    # Set Proxy
    # SOCKS_PROXY = "socks5://14ab1e7131541:39d813de77@176.103.246.143:12324" # Fixed proxy, i.e socks5://14ab1e7131541:39d813de77@176.103.246.143:12324
    # # Proxy
    # proxy_options = {}
    # proxy_options['no_proxy']= 'localhost,127.0.0.1'
    # proxy_options['http'] = SOCKS_PROXY
    # proxy_options['https'] = SOCKS_PROXY

    # seleniumwire_options['proxy'] = proxy_options
    # Set User Agent
    user_agent = UserAgent(fallback="Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36").random
    # Set Browser Option
    options = ChromeOptions()

    prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("disable-popup-blocking")
    options.add_argument("disable-notifications")
    options.add_argument("disable-popup-blocking")
    options.add_argument('--ignore-ssl-errors=yes')


    
    options.add_argument('--ignore-certificate-errors')
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options, seleniumwire_options=seleniumwire_options)
  
    return driver

def main():

    # Get website information from JSON file.
    f = open("data.json", 'r')

    data_json = json.loads(f.read())

    f.close()

    # Initialize XLSX file.
    wb = openpyxl.Workbook()
    ws = wb.active

    ws.append(FIELDNAMES)

    # Scrape Websites.
    driver = setDriver()
    for el in data_json:
    
        print(el)
        driver.get(el['url'])
        for keyword in el['keyword']:
            for click_selector in click_selectors(keyword):
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH,click_selector))).click()
                except:
                    pass
            for selector in get_selectors(keyword):
                try:
                    content_elements = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH,selector)))
                    for content_element in content_elements:
                        print(content_element.text())
                except Exception as E:
                    print(E)
                    continue

                if content != "":
                    ws.append([el['name'], keyword, content])
                    print(content)
                    break

    print("Close")

    wb.save('result.xlsx')
    driver.close()
main()