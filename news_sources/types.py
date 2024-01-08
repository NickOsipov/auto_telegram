from dataclasses import dataclass


@dataclass
class News:
    title: str
    summary: str
    img_url: str
    article_url: str


@dataclass
class HabrNewsAI(News):
    pass


class NewsColorsAndFonts:
    LINE_COLOR = "#1fb6b6"
    GRADIENT_COLOR = "#182419"
    MAIN_COLOR = "#fff"
    FONT_MAIN = "fonts/Bebas_Neue_Cyrillic.ttf"
