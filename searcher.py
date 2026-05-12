import re, json, logging, hashlib
from datetime import datetime, timedelta
from pathlib import Path

import feedparser, requests
from bs4 import BeautifulSoup

from config import (
    RSS_FEEDS, YANDEX_XML_USER, YANDEX_XML_KEY, YANDEX_QUERIES,
    YEAR_RANGE, DEDUP_DAYS
)

logger = logging.getLogger("searcher")
HASHES_FILE = Path("known_hashes.json")

# ---------- Хеши для дедупликации ----------
def load_hashes():
    if not HASHES_FILE.exists():
        return set()
    try:
        data = json.loads(HASHES_FILE.read_text(encoding="utf-8"))
        cutoff = datetime.now().strftime("%Y-%m-%d")
        fresh = {h for h, d in data.items() if d >= cutoff}
        return fresh
    except Exception:
        return set()

def save_hashes(hashes_set):
    cutoff = datetime.now().strftime("%Y-%m-%d")
    data = {}
    try:
        data = json.loads(HASHES_FILE.read_text(encoding="utf-8"))
    except Exception:
        data = {}
    for h in hashes_set:
        data[h] = cutoff
    limit = (datetime.now() - timedelta(days=DEDUP_DAYS)).strftime("%Y-%m-%d")
    data = {h: d for h, d in data.items() if d >= limit}
    HASHES_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

def object_hash(title, url):
    raw = f"{title}|{url}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()

# ---------- Обычный эвристический парсер ----------
def clean_html(raw_html):
    return BeautifulSoup(raw_html, "html.parser").get_text(separator=" ", strip=True)

def extract_fields(text, entry_title="", entry_link=""):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    title = entry_title or (lines[0] if lines else "Без названия")

    def find_field(keywords):
        for kw in keywords:
            pattern = re.compile(rf"{kw}:?\s*(.+)", re.IGNORECASE)
            m = pattern.search(text)
            if m:
                return m.group(1).strip()
        return ""

    customer     = find_field(["Заказчик", "Заказчик работ"])
    investor     = find_field(["Инвестор", "Источник финансирования", "Финансирование"])
    gen_contract = find_field(["Генеральный подрядчик", "Генподрядчик", "Подрядчик"])
    designer     = find_field(["Проектировщик", "Проектная организация", "Генпроектировщик"])

    budget = ""
    for pat in [
        r"(?:Бюджет|Стоимость|Цена контракта|НМЦК|Сметная стоимость):?\s*([\d\s]+(?:руб|₽|млн|млрд|тыс\.?\s*руб))",
        r"([\d]{1,3}(?:\s?\d{3})*(?:,\d+)?\s*(?:млн|млрд|тыс\.?\s*руб|₽|руб\.?))"
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            budget = m.group(1).strip()
            break

    start_date = ""
    for pat in [r"(?:Начало|Срок начала|Старт):?\s*(\d{2}\.\d{2}\.\d{4})",
                r"(?:с|от)\s+(\d{2}\.\d{2}\.\d{4})"]:
        m = re.search(pat, text)
        if m:
            start_date = m.group(1)
            break
    end_date = ""
    if start_date:
        rest = text[text.index(start_date)+len(start_date):]
        for p in [r"(?:до|по|—|–)\s*(\d{2}\.\d{2}\.\d{4})",
                  r"(?:Окончание|Завершение):?\s*(\d{2}\.\d{2}\.\d{4})"]:
            m2 = re.search(p, rest)
            if m2:
                end_date = m2.group(1)
                break

    return {
        "title": title,
        "customer": customer,
        "investor": investor,
        "general_contractor": gen_contract,
        "designer": designer,
        "budget": budget,
        "planned_start": start_date,
        "planned_end": end_date,
        "source_url": entry_link,
    }

# ---------- Вспомогательные функции ----------
def extract_year(text):
    m = re.search(r"(20[2-9]\d)", text)
    return int(m.group(1)) if m else None

def is_within_range(year):
    now = datetime.now().year
    return now <= year <= now + YEAR_RANGE

# ---------- Поиск по RSS ----------
def search_rss():
    results = []
    logger.info("Обход RSS-лент...")
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url, request_headers={'User-Agent': 'Mozilla/5.0'})
            for entry in feed.entries:
                try:
                    title = entry.get("title", "")
                    url   = entry.get("link", "")
                    summary = entry.get("summary", entry.get("description", entry.get("content", "")))
                    if isinstance(summary, list):
                        summary = summary[0].get("value", "") if summary else ""
                    full_text = title + " " + clean_html(summary)

                    year = extract_year(full_text)
                    if not year or not is_within_range(year):
                        continue

                    h = object_hash(title, url)
                    if h in known_hashes:
                        continue

                    data = extract_fields(full_text, title, url)
                    if data["customer"] or data["designer"] or data["general_contractor"]:
                        data["hash"] = h
                        results.append(data)
                        known_hashes.add(h)
                except Exception as e:
                    logger.warning(f"Ошибка обработки записи: {e}")
                    continue
        except Exception as e:
            logger.warning(f"Ошибка ленты {feed_url}: {e}")
    return results

# ---------- Поиск через Яндекс.XML ----------
def search_yandex():
    if not YANDEX_XML_USER or not YANDEX_XML_KEY:
        logger.info("Яндекс.XML не настроен — пропускаем.")
        return []
    results = []
    base_url = "https://yandex.ru/search/xml"
    logger.info("Обход Яндекс.XML...")
    for query in YANDEX_QUERIES:
        params = {
            "user": YANDEX_XML_USER,
            "key": YANDEX_XML_KEY,
            "query": query,
            "l10n": "ru",
            "sortby": "rlv",
            "filter": "moderate",
            "groupby": "attr=d.mode=deep.groups-on-page=10.docs-in-group=1",
        }
        try:
            resp = requests.get(base_url, params=params, timeout=15)
            soup = BeautifulSoup(resp.content, "xml")
            for group in soup.find_all("group"):
                doc = group.find("doc")
                if not doc:
                    continue
                title = (doc.find("title").text if doc.find("title") else "").strip()
                url   = (doc.find("url").text if doc.find("url") else "").strip()
                headline = doc.find("headline")
                snippet = headline.text if headline else ""
                full_text = title + " " + clean_html(snippet)

                year = extract_year(full_text)
                if not year or not is_within_range(year):
                    continue
                h = object_hash(title, url)
                if h in known_hashes:
                    continue

                data = extract_fields(full_text, title, url)
                if data["customer"] or data["designer"] or data["general_contractor"]:
                    data["hash"] = h
                    results.append(data)
                    known_hashes.add(h)
        except Exception as e:
            logger.warning(f"Ошибка Яндекс.XML по запросу '{query}': {e}")
    return results

# ---------- Главная функция ----------
known_hashes = set()

def search_all():
    global known_hashes
    known_hashes = load_hashes()
    all_results = search_rss() + search_yandex()
    save_hashes(known_hashes)
    logger.info(f"Найдено новых объектов: {len(all_results)}")
    return all_results
