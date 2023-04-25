# \Users\ELLAH\Downloads\chromedriver
# py manage.py test
# nicholas | admin
# http://localhost:8000
# http://localhost:8000/account/login/

# when to use find and get_element
from selenium import webdriver
#import time

driver = webdriver.Chrome('Users\ELLAH\Downloads\chromedriver')
driver.get('http://localhost:8000/account/login')


# //*[@id="username"]
# //*[@id="password"]
# /html/body/div/div/div/div[2]/div/div[1]/div/div/form/div[4]
# //*[@id="app"]/div[1]/div[2]/main/div[3]/button
username = driver.find_element("xpath", '//*[@id="username"]')
username.send_keys('***')
password = driver.find_element("xpath", '//*[@id="password"]')
password.send_keys('***')
login = driver.find_element("xpath", 
    '/html/body/div/div/div/div[2]/div/div[1]/div/div/form/div[4]')
login.click()

#${password}
#https://www.youtube.com/@naveenautomationlabs
#https://testersdock.com/robot-framework-database-testing/
#https://codegeex.cn
#https://codegeex.cn
#
