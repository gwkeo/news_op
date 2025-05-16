from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from transformers import pipeline
import enum
from datetime import datetime

model = pipeline(
    model="r1char9/rubert-base-cased-russian-sentiment",
)

class Tonality(enum.Enum):
    positive = 1
    neutral = 0
    negative = -1


class Comment:
    tonality: Tonality
    score: int

    def __init__(self, tonality: Tonality, score: int):
        self.tonality = tonality
        self.score = score


class Article:
    url: str
    title: str
    mid_tonality: int
    mentions_count: int

    def __init__(self, url: str, title: str, mid_tonality: int, mentions_count: int = 0):
        self.url = url
        self.title = title
        self.mid_tonality = mid_tonality
        self.mentions_count = mentions_count


def get_news(driver, url):
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')
    links = soup.select('[class^="desktop2--widget-news-desktop__mainNews"]')
    links.extend(soup.select('[class^="desktop2--card-top-avatar__rootElement"]'))
    result = []
    for i in links:
        if i.get_attribute_list('href'):
            result.append(i.get_attribute_list('href')[0])
        else:
            try:
                result.append(i.select('[class^="desktop2--card-news__titleLink"]')[0].get_attribute_list('href')[0])
            except:
                continue
    return result


def get_article(driver: webdriver.Chrome, url) -> Article:
    set_of_urls = []
    driver.get(url)
    title = driver.find_element(By.XPATH, '//a[@aria-label="Заголовок сюжета"]').text
    content = driver.page_source

    mentions_count = get_article_mentions_count(driver)

    links = get_news_url_links(content, set_of_urls)

    res = []
    for link in links:
        article = get_article_item_content(driver, link)
        article.mentions_count = mentions_count
        res.append(article)
    
    return res


def get_news_url_links(content):
    soup = BeautifulSoup(content, features='html.parser')
    sums = soup.select('[class^="news-site--StorySummarization-desktop__item"]')
    links = []
    res = []
    for i in sums:
        links = i.select('a')
        for link in links:
            a = link.get_attribute_list('href')[0]
            if 'https://dzen.ru' in a:
                res.append(link)
    return res


def get_article_mentions_count(driver: webdriver.Chrome) -> int:
    action = ActionChains(driver)
    show_more_button = driver.find_element(By.XPATH, '//button[@data-nax5mutd6="show-more"]')
    action.click(show_more_button).perform()

    show_all_button = driver.find_element(By.XPATH, '//a[@data-nax5mutd6="show-all-sources"]')
    link_to_all_sources = show_all_button.get_attribute('href')

    driver.get(link_to_all_sources)
    mentions = driver.find_elements(By.XPATH, '//article')
    return len(mentions)


def get_article_item_content(driver: webdriver.Chrome, url: str) -> Article:
    driver.get(url)
    driver.maximize_window()

    action = ActionChains(driver)
    try:
        comments_section = driver.find_element(By.XPATH, '//button[@aria-label="Показать ответы на комментарий"]')
    except:
        return
    action.move_to_element(comments_section)
    action.click(comments_section)
    action.perform()

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "comments2--root-comment__childrenContainer")]'))
        )
    except Exception:
        print(Exception)
    comments = driver.find_elements(By.XPATH, '//span[contains(@class, "comments2--rich-text__text")]')
    comments = [i.text for i in comments]

    mid_tonality = find_mid_tonality(comments)

    header = driver.find_element(By.XPATH, '//h1[@data-testid="article-title"]')


    return Article(url, header, mid_tonality)


def check_tonality(sentence) -> Comment:
    tonality = model(sentence)[0]
    t, s = Tonality.neutral, 0
    if tonality.label == 'negative':
        t = Tonality.negative
    elif tonality.label == 'positive':
        t = Tonality.positive
    s = tonality.score
    return Comment(t, s)


def find_mid_tonality(sentences: list[str]):
    mid = 0
    for i in sentences:
        comment = check_tonality(i)
        mid += comment.tonality * comment.score
    return mid


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.maximize_window()
    return driver


if __name__ == "__main__":
    driver = init_driver()
    news = get_news(driver=driver, url="https://dzen.ru/topic/moy-krasnodar")
    
    for i in news:
        get_article(driver, i)
    

