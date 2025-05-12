from parsers import dzen_parser
from drivers import chrome_driver
# from transformers import pipeline

# model = pipeline(
#     model="r1char9/rubert-base-cased-russian-sentiment",
# )


if __name__ == "__main__":
    driver = chrome_driver.init_driver()
    news = dzen_parser.get_news(driver=driver, url="https://dzen.ru/topic/moy-krasnodar")
    links = set()
    for i in news:
        links = dzen_parser.get_news_url_links(driver, i, links)
    print(links)
    print(len(links))


