from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask_testing import LiveServerTestCase
from server import create_app

chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

class MyTest(LiveServerTestCase):
    def create_app(self):
        app = create_app({"TESTING": True})
        app.config['LIVESERVER_PORT'] = 5050
        return app
      
    def test_login_logout(self):
        chrome_driver.get("http://127.0.0.1:5050")
        email_field = chrome_driver.find_element(By.NAME, 'email')
        email_field.send_keys('test@test.co')
        email_field.send_keys(Keys.ENTER)
        element = chrome_driver.find_element(By.TAG_NAME, 'h2')
        assert element.text == 'Welcome, test@test.co'

        logout = chrome_driver.find_element(By.LINK_TEXT, 'Logout')
        logout.click()
        element = chrome_driver.find_element(By.TAG_NAME, 'h1')
        assert element.text == 'Welcome to the GUDLFT Registration Portal!'
    