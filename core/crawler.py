# core/crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited = set()

def is_internal_link(base_url, link):
    return urlparse(link).netloc == "" or urlparse(link).netloc == urlparse(base_url).netloc

def crawl(url, max_depth=2):
    to_visit = [(url, 0)]
    links = []

    while to_visit:
        current_url, depth = to_visit.pop()
        if current_url in visited or depth > max_depth:
            continue

        visited.add(current_url)
        links.append(current_url)

        try:
            response = requests.get(current_url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')

            for tag in soup.find_all("a", href=True):
                link = urljoin(current_url, tag['href'])
                if is_internal_link(url, link) and link not in visited:
                    to_visit.append((link, depth + 1))

        except requests.RequestException:
            continue

    return links
