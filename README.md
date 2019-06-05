# Church database project
This project was commissioned by a local church in an effort to improve their security, especially regarding staff and members that would be around children. This project will scrape data from North Carolina Sex Offender Registry, store that data locally, and compare it to results within the church's internal database to automatically alert staff if a match has been found. 

The data of the church will be added to a gitignore file to protect the privacy and integrety of the church's members.

# Current technologies being used
This project makes use of Selenium for search automation, sqlite3 for the automatic storing of data into a local database to avoid rate-limit wait times after the initial setup, Requests to assist with API use, and BeautifulSoup to assist in webscraping.
