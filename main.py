import os
import json
import time
import requests
import bs4
import fake_headers




def write_json(dict, dir = os.getcwd(), json_name = 'result.json'):
    with open(f'{dir}/{json_name}', 'w', encoding='utf-8') as f:
        json.dump(dict, f, indent=4, sort_keys=True, ensure_ascii=False)

words_search = ','.join(('Django','Flask',))
region = (1, 2,)
page = 1
'''
'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
'''

main_url = 'https://spb.hh.ru/search/vacancy'


def main():
    pages = 1
    result = list()
    while True:

        headers = fake_headers.Headers(browser='firefox', os='win')
        headers_dict = headers.generate()
        params = {
            'text':words_search,
            'area':region,
            'order_by': 'publication_time',
            'search_period':0,
            'page':pages
        }

        response = requests.get(main_url, headers=headers_dict, params=params)
        main_html = bs4.BeautifulSoup(response.text, "lxml")

        articles_tags = main_html.find_all(class_ = 'serp-item')

        for article_tag in articles_tags:
            temp_res = list()
            link = article_tag.find(class_ = 'serp-item__title').get('href')
            company = article_tag.find('a', class_ = 'bloko-link bloko-link_kind-tertiary').get_text()

            address = list(article_tag.find(class_="vacancy-serp-item__info").children)[1].text
            if article_tag.find('span', class_ = 'bloko-header-section-3'):
                salary = article_tag.find('span', class_ = 'bloko-header-section-3').get_text()
            else:
                salary = 'не указана'

            temp_res.append({
                'ссылка':link,
                'вилка зп':salary,
                'название компании':company,
                'город':address
            })
            result.append(temp_res)
        time.sleep(0.33)
        pages +=1
        if pages >= 1:
            break





    return result

if __name__ == '__main__':
    res = main()

    write_json(res)