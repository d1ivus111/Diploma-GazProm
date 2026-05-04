import os

from page.base_page import WebPage
from page.elements import WebElement


class Dzen(WebPage):
    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN") or 'https://www.dzen.ru/'

        super().__init__(web_driver, url)

    btn_1 = WebElement(xpath='//span[@class="dzen-layout--navigation-tab__text-2g" and contains(text(), "Найти")]')
    btn_2 = WebElement(id='search-input')
    btn_3 = WebElement(xpath="//button[@aria-label='Кнопка Найти']")
    btn_4 = WebElement(xpath="(//span)[contains(text(),'Каналы')])[1]")
    btn_5 = WebElement(xpath='//[@data-testid="card-part-title" and contains(text(), "BDD. ЧТО ЭТО, ПРИМЕРЫ, ПЛЮСЫ И МИНУСЫ")]')

