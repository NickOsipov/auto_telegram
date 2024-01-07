import os
from time import sleep

from telebot import TeleBot, formatting
import requests

from new_sources.habr_news_ai_source import HabrNewsAISource


token = os.getenv("BOT_TOKEN")
bot = TeleBot(
    token=token,
    parse_mode="html",
    disable_web_page_preview=True
)
chat_id = os.getenv("CHAT_ID")
source = HabrNewsAISource()


if __name__ == "__main__":
    news_to_post = source.get_news()


    for news in news_to_post:
        photo = requests.get(news.img_url).content
        caption = source.construct_message(news=news)

        bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption
        )
        print(f"News {caption} was send")
        sleep(5)


