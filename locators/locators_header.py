from page.base_page import WebPage
import os

from page.elements import WebElement


class Header(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("HEADER") or 'https://www.gazprom.ru/'

        super().__init__(web_driver, url)

    btn_menu1 = WebElement(xpath="(//menu//a)[1]")
    btn_menu2 = WebElement(xpath="(//menu//a)[2]")
    btn_menu3 = WebElement(xpath="(//menu//a)[3]")
    btn_menu4 = WebElement(xpath="(//menu//a)[4]")
    btn_menu5 = WebElement(xpath="(//menu//a)[5]")
    btn_menu6 = WebElement(xpath="(//menu//a)[6]")
    btn_menu7 = WebElement(xpath="(//menu//a)[7]")
