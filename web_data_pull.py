from selenium import webdriver

#This uses Selenium to automatically navigate the sex offender database
# and enter each of the desired nammes
driver = webdriver.Chrome()
driver.get("http://sexoffender.ncsbi.gov/disclaimer.aspx")
driver.find_element_by_id('agree').click()
driver.find_element_by_id('lname').send_keys("James")
driver.find_element_by_id('fname').send_keys("Jones")
driver.find_element_by_id('inclaliasnames').click()
driver.find_element_by_id('searchbutton1').click()