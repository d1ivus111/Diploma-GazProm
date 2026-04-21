import requests
import allure
import pytest
import urllib3
from locators.api_locators import GazpromApiLocators

# Отключаем предупреждения SSL в консоли
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@allure.feature('API Газпром')
@allure.story('Проверка доступности ссылок хедера')
@pytest.mark.parametrize("path, description", GazpromApiLocators.HEADER_LINKS)
def test_gazprom_header_api(path, description):
    url = f"{GazpromApiLocators.BASE_URL}{path}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    with allure.step(f'API запрос к разделу хедера: {description}'):
        # Выполняем запрос с игнорированием проверки SSL сертификата
        response = requests.get(url, headers=headers, timeout=10, verify=False)

        # Проверяем, что страница отдаёт 200 OK
        assert response.status_code == 200, \
            f"Раздел '{description}' недоступен! Код: {response.status_code} по адресу {url}"

    print(f"Раздел '{description}' (API) — Пройден успешно")
