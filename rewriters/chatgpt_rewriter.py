import os

import openai
from loguru import logger


class ChatGPTRewriter:
    def rewrite_title(self, title: str) -> str:
        logger.info(f"Original title: {title}")

        return self._request(
            f"rewrite text as title of article"
            f"in one sentence and send only new version"
            f"without mention that it is a new version please.\n\n{title}"
            f"\n\nplease write it in Russian language"
        )

    def rewrite_summary(self, summary: str) -> str:
        logger.info(f"Original summary: {summary}")

        return self._request(
            f"rewrite text as summary and keep only main idea"
            f"and send only new version"
            f"without mention that it is a new version please.\n\n{summary}"
            f"\n\nplease write it in Russian language"
        )

    @staticmethod
    def _request(request_message: str) -> str:
        token = os.getenv("CHATGPT_API_KEY")
        openai.api_key = token

        completion = openai.Completion.create(
            model="gpt-3.5-turbo",
            message=[
                {
                    "role": "user",
                    "content": request_message
                }
            ]
        )

        return completion.choises[0].message.content.strip()