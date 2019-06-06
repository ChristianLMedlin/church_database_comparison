# Church database project
This project was commissioned by a local church in an effort to improve their security, especially regarding staff and members that would be around children. This project will scrape data from North Carolina Sex Offender Registry, store that data locally, and compare it to results within the church's internal database to automatically alert staff if a match has been found. 

The data of the church will be added to a gitignore file to protect the privacy and integrety of the church's members.

# Current technologies being used
This project makes use of Selenium for search automation, sqlite3 for the automatic storing of data into a local database to avoid rate-limit wait times after the initial setup, Requests to assist with API use, and BeautifulSoup to assist in webscraping.

# Segregation of code
Code that performs a specific act will be consolidated into it's appropriate .py file.
### main.py
This file will contain the core functionality of the program, such as comparing the data pulled using church_data_pull.py to the North Carolina Sex Offender Registry.
### church_data_pull.py
This will contain code written for the purpose of requesting relevant data from the Planning Center API and consolidating that within a nested dictionary. 
### web_data_pull.py
This will be used to pull any necessary HTML from the North Carolina Sex Offender Registry for us in the comparison contained within main.py
