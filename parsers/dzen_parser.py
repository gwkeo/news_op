from bs4 import BeautifulSoup

def get_news(driver, url):
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')
    links = soup.select('[class^="desktop2--widget-news-desktop__mainNews"]')
    links.extend(soup.select('[class^="desktop2--card-top-avatar__rootElement"]'))
    result = []
    for i in links:
        try:
            result.append(i.find('p').text)
        except:
            result.append(i.select('[class^="desktop2--card-news__titleLink"]')[0].get_attribute_list('title')[0])
    return result

def get_news_links(driver, url):
    driver.get(url)
    content = driver.page_source