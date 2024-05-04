# -*- coding: utf-8 -*-
"""
Created on Fri May  3 08:14:31 2024

@author: Sajad
"""

from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from jdatetime import datetime, timedelta
from prometheus_flask_exporter import PrometheusMetrics

from googletrans import Translator
# Initialize Translator object


translator = Translator()

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)


metrics = PrometheusMetrics(app)
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

@app.route('/rport/<report_count>')
# ‘/’ URL is bound with hello_world() function.
def hello_world(report_count):
         
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

        persian_date = datetime.strptime(date.text, "%Y/%m/%d %H:%M:%S")

        # Convert the jdatetime object to a Gregorian datetime object
        gregorian_date = persian_date.togregorian()
        
        print(label.text)
        print(company_name.text)
        print(date.text)
        print(gregorian_date)
        #x = {"label": label.text,"company_name": company_name.text}
        labels.append(label.text)
        company_names.append(company_name.text)
        
        string_time = gregorian_date.strftime("%Y-%m-%d %H:%M:%S")

        dates.append(string_time)


    data['label'] = labels
    data['company_name'] = company_names
    data['date'] = dates
    json_data = json.dumps(data, ensure_ascii=False)
    data_json = json.loads(json_data)

# Modify the structure if needed
# For example, let's say you want to combine the elements of each list into a single string
    modified_data = {'data': [{'label': data['label'][i], 'company_name': data['company_name'][i], 'date': data['date'][i]} for i in range(len(data['label']))] }

# Convert the modified data back to a JSON string
    modified_json = json.dumps(modified_data, ensure_ascii=False)
    modified_json = json.loads(modified_json)

    metric_name = "my_metric"
    metric = []

    for entry in modified_json['data']:
        label_value = entry['label']
        date_str = entry['date']

        # Generate Prometheus metric
        prom_metric = f"{metric_name}{{label=\"{label_value}\", date=\"{date_str}\"}} "
        metric.append(prom_metric)
    print(metric)

    return metric



@app.route('/rport/')
def hello_world_default():
    report_count = '3'  # Default value is set to 3
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

        #year, month, day = map(int, (date.text)[:10].split('/'))
        #ch_date = jdatetime.date (day=day, month=month, year=year).togregorian()
        
        persian_date = datetime.strptime(date.text, "%Y/%m/%d %H:%M:%S")

        # Convert the jdatetime object to a Gregorian datetime object
        gregorian_date = persian_date.togregorian()
        
        print(label.text)
        print(company_name.text)
        print(date.text)
        print(gregorian_date)
        #x = {"label": label.text,"company_name": company_name.text}
        labels.append(label.text)
        company_names.append(company_name.text)
        
        string_time = gregorian_date.strftime("%Y-%m-%d %H:%M:%S")
        dates.append(string_time)


    data['label'] = labels
    data['company_name'] = company_names
    data['date'] = dates
    json_data = json.dumps(data, ensure_ascii=False)
    data_json = json.loads(json_data)
    

# Modify the structure if needed
# For example, let's say you want to combine the elements of each list into a single string
    modified_data = {'data': [{'label': data['label'][i], 'company_name': data['company_name'][i], 'date': data['date'][i]} for i in range(len(data['label']))]}

# Convert the modified data back to a JSON string
    modified_json = json.dumps(modified_data, ensure_ascii=False)
    modified_json = json.loads(modified_json)
    
    metric_name = "my_metric"
    
    metric = []
    for entry in modified_json['data']:
        label_value = entry['label']
        date_str = entry['date']

        # Generate Prometheus metric
        prom_metric = f"{metric_name}{{label=\"{label_value}\", date=\"{date_str}\"}} "
        metric.append(prom_metric)
    print(metric)
    return metric

           
# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(port=8992)
