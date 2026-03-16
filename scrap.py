import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Define the list:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Header
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def parse_habr():
    url = "https://habr.com/ru/articles/"
    print("Загрузка страницы...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return

    # Find all the article cards
    articles = soup.find_all('article', class_='tm-articles-list__item')

    if not articles:
        print("Статьи не найдены. Возможно, изменилась структура HTML.")
        return

    found_articles = []

    for article in articles:
        # Extract the publication date
        time_elem = article.find('time')
        pub_date_str = time_elem.get('datetime') if time_elem else None
        if pub_date_str:
            try:
                pub_date = datetime.fromisoformat(pub_date_str)
                date_str = pub_date.strftime("%d.%m.%Y")
            except:
                date_str = "Неизв."
        else:
            date_str = "Неизв."

        # Extract the header
        title_elem = article.find('a', class_='tm-title__link')
        title = title_elem.get_text(strip=True) if title_elem else ""
        href = title_elem['href'] if title_elem and 'href' in title_elem.attrs else ""
        full_url = "https://habr.com" + href if href.startswith('/') else href

        # Description
        preview_elem = article.find('div', class_='tm-article-snippet__')
        preview_text = preview_elem.get_text(strip=True) if preview_elem else ""

        # Search
        search_text = f"{title} {preview_text}".lower()

        # Check
        if any(keyword.lower() in search_text for keyword in KEYWORDS):
            found_articles.append((date_str, title, full_url))

    # Result
    if found_articles:
        print("\nНайдено статей:", len(found_articles))
        for date_str, title, url in found_articles:
            print(f"{date_str} – {title} – {url}")
    else:
        print("Статей по ключевым словам не найдено.")

# if __name__ == "__main__"
if __name__ == "__main__":
    parse_habr()