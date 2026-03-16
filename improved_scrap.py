import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}


def get_article_text(url):
    """Download and extracts"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.find('article', class_='tm-article-body')
        if not content:
            content = soup.find('div', {'data-test': 'article-content'})

        if content:
            return content.get_text(separator=' ', strip=True).lower()
        return ''
    except Exception as e:
        print(f"Не удалось загрузить {url}: {e}")
        return ''


def parse_habr():
    url = "https://habr.com/ru/articles/"
    print("Загрузка списка статей...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Ошибка при загрузке главной страницы: {e}")
        return

    articles = soup.find_all('article', class_='tm-articles-list__item')
    if not articles:
        print("Статьи не найдены. Возможно, изменилась структура HTML.")
        return

    found_articles = []

    for i, article in enumerate(articles, 1):
        time_elem = article.find('time')
        pub_date_str = time_elem.get('datetime') if time_elem else None
        date_str = pub_date_str[:10].replace('-', '.') if pub_date_str else "Неизв."

        title_elem = article.find('a', class_='tm-title__link')
        title = title_elem.get_text(strip=True) if title_elem else ""
        href = title_elem['href'] if title_elem and 'href' in title_elem.attrs else ""
        full_url = "https://habr.com" + href if href.startswith('/') else href

        # Preview
        preview_elem = article.find('div', class_=re.compile(r'tm-article-snippet'))
        preview_text = preview_elem.get_text(strip=True).lower() if preview_elem else ""

        # Check preview
        if not any(kw.lower() in preview_text for kw in KEYWORDS):
            continue

        # Upload
        print(f"[{i}] Проверка: {title[:40]}...")
        time.sleep(0.5)
        не
        нагружать
        сервер

        full_text = get_article_text(full_url)
        if not full_text:
            search_text = preview_text
        else:
            search_text = full_text

        # Check key
        if any(kw.lower() in search_text for kw in KEYWORDS):
            found_articles.append((date_str, title, full_url))

    # Result
    print("\nНайдено статей (по полному тексту):", len(found_articles))
    for date_str, title, url in found_articles:
        print(f"{date_str} – {title} – {url}")

#if __name__=="__main"
if __name__ == "__main__":
    parse_habr()