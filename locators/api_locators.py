class GazpromApiLocators:
    BASE_URL = "https://www.gazprom.ru"

    HEADER_LINKS = [
        ("/about/", "О «Газпроме»"),
        ("/investors/", "Акционерам и инвесторам"),
        ("/press/", "Пресс-центр"),
        ("/projects/", "Проекты"),
        ("/sustainability/", "Устойчивое развитие"),
        ("/contacts/warning/", "Противодействие мошенничеству"),  # Уточненный путь
        ("/contacts/", "Контактная информация")
    ]
