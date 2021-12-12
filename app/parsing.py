import requests
from bs4 import BeautifulSoup

URL = 'https://habr.com/ru/news/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36'
}


def get_html(url, headers):
    response = requests.get(url, headers)
    return response.text


get_html(URL, HEADERS)


def parser(resp):
    data = []
    soup = BeautifulSoup(resp, 'lxml')
    div = soup.find('div', class_='tm-page__main tm-page__main_has-sidebar')
    articles_div = div.find('div', class_='tm-articles-list')
    # img_div = articles.find('div', class_='tm-article-snippet__cover tm-article-snippet__cover_cover')
    # img = img_div.find('img', class_='tm-article-snippet__lead-image').get('src')
    # description_div = div.find('div', class_='article-formatted-body article-formatted-body_version-2')
    # description = description_div.find('p').text
    # print(description)

    # a = articles_div.find_all('a', class_='tm-article-snippet__title-link')
    # for tag_a in a:
    #     title = tag_a.find('span').text
    #     data.append(title)
    #
    # news_date = articles_div.find_all('time')
    # for date in news_date:
    #     data.append(date.get('title'))
    # print(data)
    articles = soup.find_all('article', class_='tm-articles-list__item')
    for article in articles:
        title = article.find('title')


if __name__ == '__main__':
    parser(get_html(URL, HEADERS))
