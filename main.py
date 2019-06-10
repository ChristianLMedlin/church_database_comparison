from requests import get
from requests.exceptions import RequestException
from selenium import webdriver
from contextlib import closing
from bs4 import BeautifulSoup
import requests
import sqlite3
import sys
from church_data_pull import pull_data_from_API

''' Much of the code that you see here is still in development and is a work in progress. Cleanup has not been performed yet. '''

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def registry_checker(members_to_check):
    registry_driver = webdriver.Chrome()
    list_of_positives = []

    registry_driver.get('http://sexoffender.ncsbi.gov/disclaimer.aspx')
    registry_driver.find_element_by_id('agree').click()

    for members in members_to_check:
        registry_driver.find_element_by_id('lname').send_keys(members_to_check[members][1])
        registry_driver.find_element_by_id('fname').send_keys(members_to_check[members][0])
        registry_driver.find_element_by_id('inclaliasnames').click()
        registry_driver.find_element_by_id('searchbutton1').click()
        
        try:
            registry_driver.find_element_by_id('NoRowsFound')
        except:
            list_of_positives.append(members)

        registry_driver.execute_script("window.history.go(-1)")
        registry_driver.find_element_by_id('lname').clear()
        registry_driver.find_element_by_id('fname').clear()


    print(list_of_positives)
    print(len(list_of_positives))

if __name__ == '__main__':
    registry_checker(pull_data_from_API())
