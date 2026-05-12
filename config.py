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

# ========== API ЯНДЕКСА (не обязательно) ==========
YANDEX_XML_USER = ""
YANDEX_XML_KEY  = ""

# ========== КАТЕГОРИИ ОБЪЕКТОВ ==========
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
YEAR_RANGE = 4
DEDUP_DAYS = 90

# ========== ИНТЕГРАЦИЯ С ИИ DeepSeek ЧЕРЕЗ OpenRouter ==========
# Включите DeepSeek, установив USE_DEEPSEEK = True
USE_DEEPSEEK = True
# Бесплатный API-ключ с OpenRouter
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
# Бесплатная модель DeepSeek на OpenRouter
DEEPSEEK_MODEL = "deepseek/deepseek-v4-flash:free"
# API-endpoint OpenRouter (совместим с OpenAI)
DEEPSEEK_BASE_URL = "https://openrouter.ai/api/v1"
