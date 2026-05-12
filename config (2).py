import os

# ========== НАСТРОЙКИ ПОЧТЫ ==========
TO_EMAIL = "efr3mov20@yandex.ru"
SMTP_USER = "efr3mov20@yandex.ru"
FROM_EMAIL = "efr3mov20@yandex.ru"

# Пароль приложения (секретный) берётся из переменной окружения.
# GitHub Actions подставит его из секрета или из environment.
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

SMTP_HOST = "smtp.yandex.ru"
SMTP_PORT = 465

# ========== RSS-ЛЕНТЫ ==========
RSS_FEEDS = [
    "https://zakupki.gov.ru/epz/order/extendedsearch/rss.html?searchString=строительство+проектные+работы&morphology=on&openMode=USE_DEFAULT_PARAMS&page=1&sortDirection=false&sortBy=UPDATE_DATE&recordsPerPage=_50",
    "https://minstroyrf.gov.ru/press/rss/",
    "https://erzrf.ru/news/feed",
    "https://всеостройке.рф/news/feed/",
    "https://tass.ru/rss/v2.xml?sections=WyI0MzQ3Il0=",
]

# ========== API ЯНДЕКСА (если нет ключей – оставьте пустыми) ==========
YANDEX_XML_USER = ""
YANDEX_XML_KEY = ""

YANDEX_QUERIES = [
    '"концепция строительства" объект',
    '"инженерные изыскания" строительство',
    '"проектные работы" строительство объект',
    '"проектирование" госзаказ строительство',
]

YEAR_RANGE = 3
DEDUP_DAYS = 90