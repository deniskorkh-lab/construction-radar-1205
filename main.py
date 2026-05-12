# main.py
"""
Точка входа. Запускает поиск и отправляет найденное на почту Яндекс.
Запускается GitHub Actions по расписанию.
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from config import (
    TO_EMAIL, SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT, FROM_EMAIL
)
from searcher import search_all

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("main")


def format_card(obj: dict) -> str:
    """Превращает словарь с данными объекта в HTML-карточку."""
    return f"""
    <div style="border:1px solid #ccc; border-radius:8px; padding:12px; margin:10px 0; font-family:Arial,sans-serif;">
        <h3 style="margin:0 0 8px 0; color:#1a5276;">🏢 {obj.get('title', 'Без названия')}</h3>
        <table style="width:100%; border-collapse:collapse;">
            <tr><td style="padding:4px 8px;"><b>Заказчик:</b></td><td>{obj.get('customer') or '—'}</td></tr>
            <tr><td style="padding:4px 8px;"><b>Инвестор:</b></td><td>{obj.get('investor') or '—'}</td></tr>
            <tr><td style="padding:4px 8px;"><b>Генподрядчик:</b></td><td>{obj.get('general_contractor') or '—'}</td></tr>
            <tr><td style="padding:4px 8px;"><b>Проектировщик:</b></td><td>{obj.get('designer') or '—'}</td></tr>
            <tr><td style="padding:4px 8px;"><b>Бюджет:</b></td><td>{obj.get('budget') or '—'}</td></tr>
            <tr><td style="padding:4px 8px;"><b>Начало:</b></td><td>{obj.get('planned_start') or '—'}</td></tr>
            <tr><td style="padding:4px 8px;"><b>Окончание:</b></td><td>{obj.get('planned_end') or '—'}</td></tr>
        </table>
        <p style="margin-top:8px;"><a href="{obj.get('source_url', '#')}">🔗 Источник</a></p>
    </div>
    """


def send_email(html_body: str, subject: str = None):
    """Отправляет HTML-письмо через SMTP Яндекса."""
    if subject is None:
        subject = f"🏗 Строительный радар — {datetime.now().strftime('%d.%m.%Y')}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())
        logger.info(f"Письмо отправлено на {TO_EMAIL}")
    except Exception as e:
        logger.error(f"Ошибка отправки почты: {e}")
        raise


def main():
    logger.info("=== Запуск ежедневного поиска ===")
    objects = search_all()

    if not objects:
        html = """
        <div style="font-family:Arial; color:#555; padding:20px;">
            <h2>ℹ️ Новых объектов не найдено</h2>
            <p>На сегодняшний день нет новых объявлений о проектах на стадии концепции/изысканий/проектирования в заданном горизонте (+3 года).</p>
            <p>Поиск продолжается ежедневно. Следующая сводка — завтра.</p>
        </div>
        """
    else:
        cards = "".join(format_card(obj) for obj in objects)
        html = f"""
        <div style="font-family:Arial;">
            <h2>🔍 Найдено объектов: {len(objects)}</h2>
            <p style="color:#666;">Горизонт планирования: текущий год +3 года. Стадии: концепция, изыскания, проектирование (госзаказ).</p>
            {cards}
            <hr>
            <p style="font-size:12px; color:#999;">Радар работает ежедневно. Если письмо перестало приходить — проверьте настройки GitHub Actions.</p>
        </div>
        """

    send_email(html)
    logger.info("=== Готово ===")


if __name__ == "__main__":
    main()