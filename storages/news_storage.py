from typing import Hashable

from storages.base_storage import BaseStorage


class NewsStorage(BaseStorage):
    STORAGE_FILE_NAME = "news"

    def store_element(self, element: Hashable):
        data = self.get_data()
        if not data:
            data = dict()

        data[element] = element
        self.save_data(data)


if __name__ == "__main__":
    from news_sources.types import News

    news = News(title="title", summary="summary", img_url="img_url", article_url="article_url")
    storage = NewsStorage()
    storage.store_element(news)
    print(storage.get_data())
