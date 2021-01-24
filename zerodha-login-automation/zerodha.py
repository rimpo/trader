#!/usr/local/bin/python
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
import json
import pdb
import time


class ZerodhaSelenium(object):

    def __init__(self, username: str, password: str, pin: str, api_key: str):
        self.timeout = 5
        self.__username = username
        self.__password = password
        self.__pin = pin
        self.__api_key = api_key
        op = webdriver.ChromeOptions()
        op.add_argument('--headless')
        op.add_argument('--no-sandbox')
        # op.add_argument('headless')
        self.driver = webdriver.Chrome(options=op)

    def getCssElement(self, cssSelector):
        '''
        To make sure we wait till the element appears
        '''
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector)))

    def doLogin(self):
        # let's login
        self.driver.get(f"https://kite.zerodha.com/connect/login?v=3&api_key={self.__api_key}")
        try:
            passwordField = self.getCssElement("input[placeholder=Password]")
            passwordField.send_keys(self.__password)
            userNameField = self.getCssElement("input[placeholder='User ID']")
            userNameField.send_keys(self.__username)

            loginButton = self.getCssElement("button[type=submit]")
            loginButton.click()

            # 2FA
            form2FA = self.getCssElement("form.twofa-form")
            pinField = self.getCssElement("input[label='PIN']")
            pinField.send_keys(self.__pin)

            buttonSubmit = self.getCssElement("button[type=submit]")
            buttonSubmit.click()

            time.sleep(5)

        except TimeoutException:
            print("Timeout occurred")

        # pdb.set_trace()
        # close chrome
        self.driver.quit()


if __name__ == "__main__":
    api_key = os.environ["KITE_API_KEY"]
    username = os.environ["KITE_USERNAME"]
    password = os.environ["KITE_PASSWORD"]
    pin = os.environ["KITE_PIN"]

    obj = ZerodhaSelenium(username, password, pin, api_key)
    obj.doLogin()
