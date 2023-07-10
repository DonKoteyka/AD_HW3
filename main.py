
import requests
import bs4
import fake_headers
import pandas as pd



words_search = ','.join(('Django','Flask',))
region = (1, 2,)
'''
'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
'''

main_url = 'https://spb.hh.ru/search/vacancy'

result = list()
''' class="vacancy-serp-content" '''
'''
class="serp-item"

data-qa = "vacancy-serp__results" ,  id = "a11y-main-content"
зп data-qa="vacancy-serp__vacancy-compensation"
название class="serp-item__title"
ссылка href
название компании  data-qa="vacancy-serp__vacancy-employer"
город data-qa="vacancy-serp__vacancy-address"
'''

headers = fake_headers.Headers(browser='firefox', os='win')
headers_dict = headers.generate()
params = {
    'text':words_search,
    'area':region

}

response = requests.get(main_url, headers=headers_dict, params=params)
main_html = bs4.BeautifulSoup(response.text, "lxml")

articles_tags = main_html.find_all(class_ = 'serp-item')

for article_tag in articles_tags:
    name_vacancy = article_tag.find(target ="_blank")
    link = article_tag.find(class_ = 'serp-item__title').get('href')
    company = article_tag.find(class_ = 'bloko-text')
    print()









if __name__ == '__main__':
    print(articles_tags)