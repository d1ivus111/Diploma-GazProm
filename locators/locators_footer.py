import os

from page.base_page import WebPage
from page.elements import WebElement


class Footer(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("FOOTER") or 'https://www.gazprom.ru/'

        super().__init__(web_driver, url)

    btn_footer1 = WebElement(xpath='(//footer//*[@target="_blank"])[1]')
    btn_footer2 = WebElement(xpath='(//footer//*[@target="_blank"])[2]')
    btn_footer3 = WebElement(xpath='(//footer//a)[3]')
    btn_footer4 = WebElement(xpath='(// footer // a)[4]')
    btn_footer5 = WebElement(xpath='(//*[@noindex="true"])[10]')
    btn_footer6 = WebElement(xpath='(// footer // a)[6]')