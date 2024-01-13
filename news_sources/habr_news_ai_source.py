from typing import List, Any
from datetime import datetime as dt, date

from bs4 import BeautifulSoup

from news_sources.base_news_source import BaseNewsSource
from news_sources.types import HabrNewsAI


class HabrNewsAISource(BaseNewsSource):
    SOURCE_MAIN_URL = "https://habr.com"
    SOURCE = "Habr"
    HASHTAG = "#AI"

    def __init__(self):
        super().__init__(
            url="https://habr.com/ru/hubs/artificial_intelligence/articles/"
        )

    def _get_raw_today_news(self) -> List[Any]:
        return self.parsed_source.find_all(
            name="article", attrs={"class": "tm-articles-list__item"}
        )

    def _map_raw_news(self, raw_news: List[Any]) -> List[HabrNewsAI]:
        result = []
        for idx_news, raw_one_news in enumerate(raw_news, 1):
            article_url = self._get_article_url(raw_news=raw_one_news)
            article_soup = self._get_article_soup(article_url=article_url)
            try:
                # if not self._is_fresh_article(article_soup):
                #     print(True)
                #     break
                title = self._get_title(article_soup)
                summary = self._get_summary(article_soup)
                img_url = self._get_image_url(article_soup)
                result.append(
                    HabrNewsAI(
                        title=title,
                        summary=summary,
                        img_url=img_url,
                        article_url=article_url,
                    )
                )
            except Exception as e:
                pass
        return result

    def _get_article_url(self, raw_news: BeautifulSoup) -> str:
        url_end = raw_news.find(
            name="a", attrs={"class": "tm-title__link", "data-article-link": "true"}
        )
        url_end = url_end.attrs["href"]
        url_result = f"{self.SOURCE_MAIN_URL}{url_end}"
        return url_result

    def _get_article_date(self, raw_news: BeautifulSoup) -> date:
        article_datetime = raw_news.find(
            name="span", attrs={"class": "tm-article-datetime-published"}
        )
        article_datetime = article_datetime.find("time").attrs["datetime"]
        article_datetime = dt.strptime(article_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")
        article_date = article_datetime.date()
        return article_date

    def _get_title(self, article_soup: BeautifulSoup) -> str:
        title = article_soup.find("title").text.strip(" / Хабр")
        return title

    def _get_summary(self, article_soup: BeautifulSoup) -> str:
        summary = article_soup.find(name="div", attrs={"id": "post-content-body"})
        try:
            summary = summary.find("p").text
        except:
            summary = None
        return summary

    def _get_image_url(self, article_soup: BeautifulSoup) -> str:
        img_url = article_soup.find(name="div", attrs={"id": "post-content-body"})
        try:
            img_url = img_url.find("img").attrs["data-src"]
        except:
            img_url = img_url.find("img").attrs["src"]
        return img_url


if __name__ == "__main__":
    source = HabrNewsAISource()
    print(source.get_news())
