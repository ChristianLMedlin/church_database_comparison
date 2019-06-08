from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import sqlite3
import sys
import time
from API_Auth import create_key, create_secret, create_login, create_password


#Returns the total number of members in the church's Planning Center database for use as the upper range limit in the pull_data_from_API function.
def get_number_of_visitors():
    login = create_login()
    password = create_password()

    driver = webdriver.Chrome()
    
    driver.get('https://accounts.planningcenteronline.com/?return=People%2F')
    driver.find_element_by_id('email').send_keys(login)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_name('commit').click()

    number_of_visitors = driver.find_element_by_class_name('chart-total').get_attribute('innerHTML')
    number_of_visitors = ''.join(number for number in number_of_visitors if number.isnumeric())
    return(int(number_of_visitors) + 1)


#Retrieves the appropriate data from the API for use in the store_items_in_database function.
#This function pulls the data from the API and returns the items in a dictionary where the key is the full name and the value is a list containing the first_name and last_name
def pull_data_from_API():
    #The value of these variables should be replaced with your respective Key and Secret if you wish to use the Planning Center API.

    my_key = create_key()
    my_secret = create_secret()
    params = (
        ('order', 'created_at'),
        ('per_page', '50'),
    )
    dict_of_members = {}
    number_of_visitors = get_number_of_visitors()

    for offset_number in range(0, number_of_visitors, 49):
        received_json = requests.get(f'''https://api.planningcenteronline.com/people/v2/people?offset={offset_number}''', params=params, auth=(my_key, my_secret)).json()
        try:
            for data_index in range(len(received_json["data"])):
                first_name = ''.join(name.lower() for name in received_json["data"][data_index]["attributes"]['first_name'] if name.isalpha())
                last_name =  ''.join(name.lower() for name in received_json["data"][data_index]["attributes"]['last_name'] if name.isalpha())
                full_name = first_name + ' ' + last_name

                dict_of_members[full_name] = [first_name, last_name]
        except:
            print("It broke.")
            print(len(dict_of_members))

        print(len(dict_of_members))
        time.sleep(2)
    print(dict_of_members)
    print(len(dict_of_members))
    return dict_of_members


#Creating an object for use in indexing data into the database
def store_items_in_database(json_data):
    church_data_connection = sqlite3.connect('church_data.db')
    data_cursor = church_data_connection.cursor()
    data_cursor.execute(''' CREATE TABLE IF NOT EXISTS church_members (ID INTEGER PRIMARY KEY AUTOINCREMENT, first_name VARCHAR(100), last_name VARCHAR(100), full_name VARCHAR(200)) ''')

    #for i in range(float('inf')):

    for id_number in range(len(json_data["data"])):
        first_name = json_data["data"][id_number]["attributes"]['first_name']
        last_name = json_data["data"][id_number]["attributes"]['last_name']
        full_name = json_data["data"][id_number]["attributes"]['name']
    #Make sure to add an IF statement to check whether or not a fullname is already in the database.
        data_cursor.execute(''' INSERT INTO church_members (first_name, last_name, full_name) VALUES(?, ?, ?) ''', (first_name, last_name, full_name))

    for row in data_cursor.execute(''' SELECT * FROM church_members '''):
        print(row)

    # for row in data_cursor.execute(''' SELECT ID FROM church_members ORDER BY ID DESC LIMIT 1 '''):
    #     print(row)
