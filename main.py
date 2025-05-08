from parsers import dzen_parser
from drivers import chrome_driver
from transformers import pipeline

model = pipeline(
    model="r1char9/rubert-base-cased-russian-sentiment",
)

if __name__ == "__main__":
    driver = chrome_driver.init_driver()
    news = dzen_parser.get_news(driver=driver, url="https://dzen.ru/topic/moy-krasnodar")
    for i in news:
        print(i, model(i))
        print()
    print(len(news))