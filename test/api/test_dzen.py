import time
import allure
from locators.locators_dzen import Dzen
from conftest import web_browser


@allure.feature('UI Tests')
@allure.title('Тест')
def test_dzen(web_browser):
    page = Dzen(web_browser)
    page.btn_1.click()
    time.sleep(3)
    page.btn_2.send_keys('YellowSun Testing')
    page.btn_3.click()
    page.btn_4.click()
    page.btn_5.click()
    page.switch_to_window(1)
    time.sleep(1)
    time.sleep(5)
    page.btn_6.click()
    page.btn_7.click()
    time.sleep(2)
