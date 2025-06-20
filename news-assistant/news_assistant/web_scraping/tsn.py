import requests
from bs4 import BeautifulSoup
from news_assistant.model.article import Article


class TsnScrapper:

    def scrap_url(self, url):
        article = None

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')

            article = Article(title=self.get_title(soup),
                              content=self.get_content(soup),
                              summary=None,
                              topics=None,
                              url=url)
        except Exception as e:
            raise RuntimeError("An error occurred during News article loading") from e

        return article

    def get_title(self, soup):
        title = None

        for tag in soup.find("h1", class_="c-entry__title"):
            title = tag.get_text(strip=True)

        return title

    def get_content(self, soup):
        paragraphs = []

        for tag in soup.find("div", class_="c-post__inner"):
            if tag.name == "p":
                paragraphs.append(tag.get_text(strip=True))

        return paragraphs
