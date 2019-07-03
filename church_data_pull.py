from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
import requests
import sqlite3
import sys
import time
from API_Auth import create_key, create_secret, create_login, create_password


#Returns the total number of members in the church's Planning Center database for use as the upper range limit in the pull_data_from_API function.
def get_number_of_visitors():
    login = create_login()
    password = create_password()
    visitor_driver = webdriver.Chrome()
    
    visitor_driver.get('https://accounts.planningcenteronline.com/?return=People%2F')
    visitor_driver.find_element_by_id('email').send_keys(login)
    visitor_driver.find_element_by_id('password').send_keys(password)
    visitor_driver.find_element_by_name('commit').click()

    number_of_visitors = visitor_driver.find_element_by_class_name('chart-total').get_attribute('innerHTML')
    number_of_visitors = ''.join(number for number in number_of_visitors if number.isnumeric())
    return(int(number_of_visitors) + 1)

#Uses a member's date of birth to find their current age and returns it.
def return_age(date_of_birth):
    birth_year = int(date_of_birth[0:4])
    birth_month = int(date_of_birth[5:7])
    birth_day = int(date_of_birth[8:])

    today = date.today()
    return today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))

#Retrieves the appropriate data from the API for use in the store_items_in_database function.
#This function pulls the data from the API and returns the items in a dictionary where the key is the full name and the value is a list containing the first_name, last_name, and age.
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
                date_of_birth = received_json["data"][data_index]["attributes"]["birthdate"]
                full_name = first_name + ' ' + last_name

                if date_of_birth != None:
                    age = return_age(date_of_birth)

                    if age > 0:
                        dict_of_members[full_name] = [first_name, last_name, age]
        except:
            #This section should either be removed or it should E-Mail the appropriate person to alert them of a fatal change in the API.
            print("It broke.")
            print(len(dict_of_members))

        print(len(dict_of_members))
        time.sleep(2)
    print(len(dict_of_members))
    return dict_of_members


#Creating an object for use in indexing data into the database
# def store_items_in_database(json_data):
#     church_data_connection = sqlite3.connect('church_data.db')
#     data_cursor = church_data_connection.cursor()
#     data_cursor.execute(''' CREATE TABLE IF NOT EXISTS church_members (ID INTEGER PRIMARY KEY AUTOINCREMENT, first_name VARCHAR(100), last_name VARCHAR(100), full_name VARCHAR(200)) ''')

#     #for i in range(float('inf')):

#     for id_number in range(len(json_data["data"])):
#         first_name = json_data["data"][id_number]["attributes"]['first_name']
#         last_name = json_data["data"][id_number]["attributes"]['last_name']
#         full_name = json_data["data"][id_number]["attributes"]['name']
#     #Make sure to add an IF statement to check whether or not a fullname is already in the database.
#         data_cursor.execute(''' INSERT INTO church_members (first_name, last_name, full_name) VALUES(?, ?, ?) ''', (first_name, last_name, full_name))

#     for row in data_cursor.execute(''' SELECT * FROM church_members '''):
#         print(row)

#     # for row in data_cursor.execute(''' SELECT ID FROM church_members ORDER BY ID DESC LIMIT 1 '''):
#     #     print(row)
