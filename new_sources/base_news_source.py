from typing import Dict, List
from abc import ABC, abstractmethod

from telebot import formatting
from bs4 import BeautifulSoup
import requests
from fake_useragent import FakeUserAgent

from new_sources.types import News


class BaseNewsSource(ABC):
    SOURCE = ""

    def __init__(self, url: str):
        self.parsed_source = BeautifulSoup(
            requests.get(
                url=url,
                headers=self._get_headers()
            ).content,
            features="lxml"
        )

    def get_news(self) -> List[News]:
        raw_news = self._get_raw_today_news()
        return self._map_raw_news(raw_news)

    def construct_message(self, news: News) -> str:
        title = news.title.strip().rstrip("\n")
        title = formatting.hbold(title)
        if news.summary is not None:
            summary = f"\n{news.summary.strip()}\n"
        else:
            summary = ""
        link = formatting.hlink(content="Подробнее", url=news.article_url)
        text_message = f"{title}\n{summary}\n{link}\n\n{self.SOURCE}"

        return text_message

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        ua = FakeUserAgent()

        return {
            "User-Agent": ua.random
        }

    @abstractmethod
    def _get_raw_today_news(self) -> List[BeautifulSoup]:
        pass

    @abstractmethod
    def _map_raw_news(self, raw_news: List[BeautifulSoup]) -> List[News]:
        pass

    @abstractmethod
    def _get_article_url(self, raw_news: BeautifulSoup) -> str:
        pass

    def _get_article_soup(self, article_url: str) -> BeautifulSoup:
        return BeautifulSoup(
            requests.get(
                url=article_url,
                headers=self._get_headers(),
            ).content,
            features='lxml'
        )

    @abstractmethod
    def _get_title(self, article_soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_summary(self, article_soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_image_url(self, article_soup: BeautifulSoup) -> str:
        pass