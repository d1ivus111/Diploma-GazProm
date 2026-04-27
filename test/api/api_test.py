import requests
import pytest
import time

BASE_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_price(coin_id):
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }

    for attempt in range(5):  # больше попыток
        r = requests.get(BASE_URL, params=params, timeout=10)

        if r.status_code == 200:
            return r

        if r.status_code == 429:
            time.sleep(2 + attempt)  # увеличиваем ожидание

    pytest.skip("пропуск из-за rate limit API")


@pytest.mark.parametrize("coin_id, min_price", [
    ("bitcoin", 30000),
    ("ethereum", 1000),
    ("solana", 10)
])
def test_coingecko_simple(coin_id, min_price):
    response = get_price(coin_id)

    data = response.json()

    assert coin_id in data

    price = data[coin_id]["usd"]

    assert isinstance(price, (int, float))
    assert price > min_price
