import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

@allure.feature('UI Tests')
def test_dzen(web_browser):
    page = Dzen(web_browser)
    page.btn_1.click()
    time.sleep(3)
    page.btn_2.send_keys('halibut testing')
    page.btn_3.click()
    page.btn_4.click()
    page.btn_5.click()
    page.switch_to_window(1)
    time.sleep(2)
    time.sleep(5)
