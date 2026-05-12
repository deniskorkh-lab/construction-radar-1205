import os

# ========== ПОЧТА ==========
TO_EMAIL   = "efr3mov20@yandex.ru"
SMTP_USER  = "efr3mov20@yandex.ru"
FROM_EMAIL = "efr3mov20@yandex.ru"
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_HOST  = "smtp.yandex.ru"
SMTP_PORT  = 465

# ========== RSS-ЛЕНТЫ (госзакупки, минстрой, новости) ==========
RSS_FEEDS = [
    "https://zakupki.gov.ru/epz/order/extendedsearch/rss.html?searchString=строительство+проектные+работы&morphology=on&openMode=USE_DEFAULT_PARAMS&page=1&sortDirection=false&sortBy=UPDATE_DATE&recordsPerPage=_50",
    "https://minstroyrf.gov.ru/press/rss/",
    "https://erzrf.ru/news/feed",
    "https://всеостройке.рф/news/feed/",
    "https://tass.ru/rss/v2.xml?sections=WyI0MzQ3Il0=",
]

# ========== ПОИСК ЧЕРЕЗ ЯНДЕКС (БЕЗ КЛЮЧА – ТОЛЬКО RSS) ==========
YANDEX_XML_USER = ""
YANDEX_XML_KEY  = ""

# ========== КАТЕГОРИИ ОБЪЕКТОВ (ДЛЯ ФОРМИРОВАНИЯ ЗАПРОСОВ) ==========
CATEGORIES = [
    "жилая недвижимость",
    "социально-культурная недвижимость",
    "многоквартирный дом",
    "административное здание",
    "спортивный объект",
    "коммерческая недвижимость",
    "образовательное учреждение",
    "офисное здание",
    "лечебное учреждение",
    "торговый центр",
    "театр",
    "кинотеатр",
    "гостиница",
    "СТО",
    "социальное строительство",
    "апартаменты",
    "апарт-отель",
    "МФК",
    "инфраструктурный объект",
    "промышленная недвижимость",
    "производственный комплекс",
    "паркинг",
]

# Автоматически генерируем поисковые фразы для Яндекса
YANDEX_QUERIES = [
    f'"проектирование" "{cat}" строительство'
    for cat in CATEGORIES
] + [
    f'"изыскания" "{cat}" объект'
    for cat in CATEGORIES
] + [
    f'"концепция строительства" "{cat}"'
    for cat in CATEGORIES
]

# ========== ГОРИЗОНТ ПОИСКА ==========
# Ищем объекты, у которых год начала работ попадает в [текущий год, текущий год + 4]
YEAR_RANGE = 4

# Дней помнить дубликаты
DEDUP_DAYS = 90

# ========== ИНТЕГРАЦИЯ С ИИ ЯНДЕКСА (ОПЦИОНАЛЬНО) ==========
# Если хотите улучшить извлечение сущностей через Yandex GPT,
# получите ключ в Yandex Cloud (https://console.cloud.yandex.ru/)
# и заполните поля ниже.
YANDEX_GPT_KEY    = ""   # API-ключ сервисного аккаунта
YANDEX_GPT_FOLDER = ""   # Идентификатор каталога
USE_YANDEX_GPT    = False # Переключите на True, когда заполните ключ
