import allure

from locators.locators_header import Header
from conftest import web_browser

def test_main_header(web_browser):
    page = Header(web_browser)
    if page.btn_menu1.is_clickable():
        page.btn_menu1.click(3)

    page.btn_menu1.click(3)

    data = [
        (page.btn_menu1, "Кнопка О «Газпроме»"),
        (page.btn_menu2, "Кнопка Акционерам и инвесторам"),
        (page.btn_menu3, "Кнопка Пресс-центр"),
        (page.btn_menu4, "Кнопка Проекты"),
        (page.btn_menu5, "Кнопка Устойчивое развитие"),
        (page.btn_menu6, "Кнопка Противодействие мошенничеству"),
        (page.btn_menu7, "Кнопка Контактная информация"),
    ]

    for btn, text in data:
        with allure.step(f'Проверка кликабельности {text}'):
            assert btn.is_clickable(), f'некликабельна {text}'