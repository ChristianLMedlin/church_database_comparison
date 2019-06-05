from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import requests
import sqlite3
import sys
from API_Auth import create_key, create_secret

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

my_key = create_key()
my_secret = create_secret()

params = (
    ('order', 'created_at'),
    ('per_page', '100'),
)

response = requests.get('https://api.planningcenteronline.com/people/v2/people', params=params, auth=(my_key, my_secret)).json()

#Retrieves the appropriate data from the API for use in the store_items_in_database function.
def get_data_from_API():
    pass


#Creating an object for use in indexing data into the database
def store_items_in_database(json_data):
    church_data_connection = sqlite3.connect('church_data.db')
    data_cursor = church_data_connection.cursor()
    data_cursor.execute(''' CREATE TABLE IF NOT EXISTS church_members (ID INTEGER PRIMARY KEY AUTOINCREMENT, first_name VARCHAR(100), last_name VARCHAR(100), full_name VARCHAR(200)) ''')

    for id_number in range(len(json_data["data"])):
        first_name = json_data["data"][id_number]["attributes"]['first_name']
        last_name = json_data["data"][id_number]["attributes"]['last_name']
        full_name = json_data["data"][id_number]["attributes"]['name']
    #Make sure to add an IF statement to check whether or not a fullname is already in the database.
        data_cursor.execute(''' INSERT INTO church_members (first_name, last_name, full_name) VALUES(?, ?, ?) ''', (first_name, last_name, full_name))

    for row in data_cursor.execute(''' SELECT * FROM church_members '''):
        print(row)


store_items_in_database(response)
