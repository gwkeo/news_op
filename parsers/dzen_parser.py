from bs4 import BeautifulSoup


def get_news(driver, url):
    try:
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, features='html.parser')
        links = soup.select('[class^="desktop2--widget-news-desktop__mainNews"]')
        links.extend(soup.select('[class^="desktop2--card-top-avatar__rootElement"]'))
        links.extend(soup.select('[class^="desktop2--card-horizontal-news__cardLink"]'))
        result = []
        for i in links:
            if i.get_attribute_list('href'):
                result.append(i.get_attribute_list('href')[0])
            else:
                try:
                    result.append(i.select('[class^="desktop2--card-news__titleLink"]')[0].get_attribute_list('href')[0])
                except:
                    continue
    except:
        print(f"something went wrong: '{i}'")
    return result


def get_news_url_links(driver, url, set_of_urls):
    try:
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
    except:
        raise Exception("something went wrong")


