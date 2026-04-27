import allure
from locators.locators_header import Header
from conftest import web_browser


@allure.title('Header test')
@allure.feature('UI Gazprom header test')
def test_main_header(web_browser):
    page = Header(web_browser)

    data = [
        (page.btn_menu1, "Кнопка О «Газпроме»", "about"),
        (page.btn_menu2, "Кнопка Акционерам и инвесторам", "investors"),
        (page.btn_menu3, "Кнопка Пресс-центр", "press"),
        (page.btn_menu4, "Кнопка Проекты", "projects"),
        (page.btn_menu5, "Кнопка Устойчивое развитие", "sustainability"),
        (page.btn_menu6, "Кнопка Противодействие мошенничеству", "warning"),
        (page.btn_menu7, "Кнопка Контактная информация", "contacts"),
    ]

    for btn, text, expected_url_part in data:
        with allure.step(f'Проверка ссылки: {text}'):
            assert btn.is_clickable(), f'Некликабельна {text}'
            btn.click()

            current_url = web_browser.current_url
            assert expected_url_part in current_url, \
                f'Неверный URL у {text}: {current_url}'

            web_browser.back()