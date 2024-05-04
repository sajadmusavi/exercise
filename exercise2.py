# -*- coding: utf-8 -*-
"""
Created on Fri May  3 08:14:31 2024

@author: Sajad
"""

from flask import Flask
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/rport/<report_count>')
# ‘/’ URL is bound with hello_world() function.
def hello_world(report_count):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import pandas as pd
    import jdatetime
    import json
    from datetime import datetime




            
    driver = webdriver.Chrome()
    driver.get('https://codal.ir/')


    search_result = driver.find_elements(By.CLASS_NAME ,"table__row")
    search_result = search_result[ : int(report_count)]

    data = {}
    labels = []
    company_names = []
    dates = []



    for result in search_result:
        label = result.find_element(By.XPATH , './/td[1]/a/strong')
        company_name = result.find_element(By.XPATH , './/td[2]/span')
        date = result.find_element(By.XPATH , './/td[7]/span')

        year, month, day = map(int, (date.text)[:10].split('/'))
        ch_date = jdatetime.date (day=day, month=month, year=year).togregorian()
        
        print(label.text)
        print(company_name.text)
        print(date.text)
        print(ch_date)
        #x = {"label": label.text,"company_name": company_name.text}
        labels.append(label.text)
        company_names.append(company_name.text)
        
        string_time = ch_date.strftime("%Y-%m-%d")
        dates.append(string_time)


    data['label'] = labels
    data['company_name'] = company_names
    data['date'] = dates
    json_data = json.dumps(data, ensure_ascii=False)
    print(json_data)
    return json_data
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
