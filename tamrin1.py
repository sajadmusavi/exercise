# -*- coding: utf-8 -*-
"""
Created on Thu May  2 10:03:04 2024

@author: Sajad
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from jdatetime import datetime, timedelta

driver = webdriver.Chrome()
driver.get('https://codal.ir/')


search_result = driver.find_elements(By.XPATH ,'.//*[@id="divLetterFormList"]/table/tbody/tr[1]')


for result in search_result:
    label = result.find_element(By.XPATH , './/td[1]/a/strong')
    company_name = result.find_element(By.XPATH , './/td[2]/span')
    date = result.find_element(By.XPATH , './/td[7]/span')

    persian_date = datetime.strptime(date.text, "%Y/%m/%d %H:%M:%S")

    # Convert the jdatetime object to a Gregorian datetime object
    gregorian_date = persian_date.togregorian()

    print(label.text)
    print(company_name.text)
    print(date.text)
    print(gregorian_date)
