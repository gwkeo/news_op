from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from transformers import pipeline

model = pipeline(
    model="r1char9/rubert-base-cased-russian-sentiment",
)


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


def get_news_url_links(driver, url, set_of_urls):
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')
    articles = soup.select('[class^="news-site--StorySummarization-desktop__item"]')
    links = []
    for i in articles:
        links = i.select('a')
        for link in links:
            a = link.get_attribute_list('href')[0]
            if 'dzen.ru' in a:
                set_of_urls.add(a)
    return set_of_urls


def get_article_item_content(driver: webdriver.Chrome, url):
    driver.get(url)
    content = driver.page_source
    driver.maximize_window()

    action = ActionChains(driver)
    try:
        comments_section = driver.find_element(By.XPATH, '//button[@aria-label="Показать ответы на комментарий"]')
    except:
        return
    action.move_to_element(comments_section)
    action.click()
    action.perform()

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "comments2--root-comment__childrenContainer")]'))
        )
    except:
        print(f"{url} wasn't parsed. Timeout")
        return
    comments = driver.find_elements(By.XPATH, '//span[contains(@class, "comments2--rich-text__text")]')
    comments = [i.text for i in comments]
    return comments


    # commentsDiv = soup.select('div[data-testid="article-comments"]).scrollIntoView()')[0]
    # comments = commentsDiv.select('span')
    # for i in comments:
    #     print(i)


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.maximize_window()
    return driver


def parse(driver: webdriver.Chrome, url):
    driver.get(url)
    content = driver.page_source
    return content


if __name__ == "__main__":
    driver = init_driver()
    news = get_news(driver=driver, url="https://dzen.ru/topic/moy-krasnodar")
    links = set()
    for i in news:
        links = get_news_url_links(driver, i, links)
    
    for i in links:
        comments = get_article_item_content(driver, i)
        if comments:
            for i in comments:
                if i:
                    print(i, model(i))

    print(links)
    print(len(links))