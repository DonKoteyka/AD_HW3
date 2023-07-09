import re
import time

import requests
import bs4
import fake_headers
import pandas as pd

words_search = '|'.join(('дизайн', 'фото', 'web', 'python',))
result = list()

headers = fake_headers.Headers(browser='firefox', os='win')
headers_dict = headers.generate()
response = requests.get('https://habr.com/ru/all/', headers=headers_dict)
main_html_data = response.text
main_html = bs4.BeautifulSoup(main_html_data, "lxml")
articles_tag = main_html.find('div', class_ = 'tm-article-list')
articles_tags = main_html.find_all('article')
for article_tag in articles_tags[1:]:
    h2_tag = article_tag.find('h2')
    a_tag = h2_tag.find('a')
    span_tag = a_tag.find('span')
    time_tag = article_tag.find('time')

    link = 'https://habr.com'+a_tag.get('href')
    title = span_tag.text
    date_time = time_tag['datetime']
    response = requests.get(link, headers=headers.generate()).text
    article_html = bs4.BeautifulSoup(response, "lxml")
    article_full_tag = article_html.find('div', id="post-content-body")
    article_full_tag_text = article_full_tag.text

    if bool(re.search(words_search, article_full_tag_text, flags=re.I)) or bool(re.search(words_search, title, flags=re.I)):
        result.append({'title':title, 'link': link, 'date_time': date_time, 'text':article_full_tag_text})
    time.sleep(0.5)


if __name__ == '__main__':
    print(pd.DataFrame(result))
