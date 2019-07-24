from requests import get
from requests.exceptions import RequestException
from selenium import webdriver
from contextlib import closing
import requests
import sqlite3
import sys
from church_data_pull import pull_data_from_API
from API_Auth import create_email, create_email_pass, create_target_email
import smtplib, ssl
from datetime import date

''' Much of the code that you see here is still in development and is a work in progress. Cleanup has not been performed yet. '''


#This uses Selenium to search through the NC Registry and appends any matches to a list
def registry_checker(members_to_check):
    registry_driver = webdriver.Chrome()
    list_of_positives = []

    registry_driver.get('http://sexoffender.ncsbi.gov/disclaimer.aspx')
    registry_driver.find_element_by_id('agree').click()

    for members in members_to_check:
        registry_driver.find_element_by_id('lname').send_keys(members_to_check[members][1])
        registry_driver.find_element_by_id('fname').send_keys(members_to_check[members][0])
        registry_driver.find_element_by_id('age').send_keys(members_to_check[members][2])
        registry_driver.find_element_by_id('inclaliasnames').click()
        registry_driver.find_element_by_id('searchbutton1').click()
        
        try:
            registry_driver.find_element_by_id('NoRowsFound')
        except:
            list_of_positives.append(members)

        registry_driver.execute_script("window.history.go(-1)")
        registry_driver.find_element_by_id('lname').clear()
        registry_driver.find_element_by_id('fname').clear()
        registry_driver.find_element_by_id('age').clear()

    return list_of_positives

def email_setup():
    names = registry_checker(pull_data_from_API())

    context = ssl.create_default_context()
    message = f"""\
Subject: Automated Search results {date.today()}


The search has returned {len(names)} potential matches, check the following names: 

{names}

Any newly matched names will appear at the end of the list.
The NC Sex Offender Registry matches names that are similar in spelling to other names, this allows the system to account for typos as the expense of a few more false positives.
If this system needs maintenance or you would like it to be changed in some way, contact ChristianLMedlin@gmail.com
"""

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(create_email(), create_email_pass())
        server.sendmail(create_email(), create_target_email(), message)


if __name__ == '__main__':
    email_setup()