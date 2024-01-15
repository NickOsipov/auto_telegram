import os
from time import sleep
from loguru import logger

from telebot import TeleBot, formatting
import requests

from news_sources.habr_news_ai_source import HabrNewsAISource


token = os.getenv("BOT_TOKEN")
bot = TeleBot(token=token, parse_mode="html", disable_web_page_preview=True)
chat_id = os.getenv("CHAT_ID")
news_to_post = int(os.environ.get("NEWS_TO_POST") or 3)
attempts = 3
source = HabrNewsAISource()


if __name__ == "__main__":
    logger.info(f"News to post: {news_to_post}")

    while news_to_post:
        if not attempts:
            break
        print("news_to_post:", news_to_post)
        news = source.get_one_news()
        if not news:
            print("not news")
            print("attempts:", attempts)
            attempts -= 1
            continue

        photo = source.create_mem_from_photo(news=news)
        caption = source.construct_caption(news=news)

        bot.send_photo(
            chat_id=chat_id,
            photo=open(photo, 'rb'),
            caption=caption
        )
        logger.info(f"News {news.title} was sent")
        photo.unlink()
        sleep(5)
        news_to_post -= 1

