from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    return webdriver.Chrome(options=options)

def get_news(driver, url):
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')
    links = soup.select('[class^="desktop2--card-top-avatar__rootElement"]')
    result = []
    for i in links:
        result.append(i.find('p').text)
    return result

if __name__ == "__main__":
    driver = init_driver()
    news = get_news(driver=driver, url="https://dzen.ru/topic/moy-krasnodar")
    for i in news:
        print(i)
    print(len(i))