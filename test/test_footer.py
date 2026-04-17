import allure
from locators.locators_footer import Footer
from conftest import web_browser

@allure.title('Footer test')
@allure.feature('UI Gazprom footer test')
def test_main_footer(web_browser):
    page = Footer(web_browser)

    data = [
        (page.btn_footer1, "Сделано в Студия Артемия Лебедева", "artlebedev"),
        (page.btn_footer2, "Информация о сайте", "site3"),
        (page.btn_footer3, "Контактная информация", "contacts"),
        (page.btn_footer4, "Карта сайта", "map"),
        (page.btn_footer5, "Раскрытие информации", "PORTAL"),
        (page.btn_footer6, "Доступность информации", "accessibility"),
    ]

    for btn, text, expected_url_part in data:
        with allure.step(f'Проверка ссылки: {text}'):

            assert btn.is_clickable(), f'Некликабельна {text}'

            original_window = web_browser.current_window_handle
            old_windows = web_browser.window_handles

            btn.click()