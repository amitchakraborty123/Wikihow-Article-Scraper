'''
Author: Amit Chakraborty
Project: Wikihow Article Scraper
Profile URL: https://github.com/amitchakraborty123
E-mail: mr.amitc55@gmail.com
'''


import os
import time
import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

x = datetime.datetime.now()
n = x.strftime("__%b_%d_%Y")


def get_category_link():
    print('=================== Getting Category Link ===================')
    all_links = []
    url = 'https://www.wikihow.com/Special:Sitemap'
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    lis = soup.find('div', {'id': 'cat_outer'}).find_all('li')
    for li in lis:
        try:
            ll = 'https://www.wikihow.com' + li.find('a')['href']
            new_link = {
                'links': ll,
            }
            # print(link)
            if new_link not in all_links:
                all_links.append(new_link)
                df = pd.DataFrame([new_link])
                df.to_csv('Category_Links.csv', mode='a', header=not os.path.exists('Category_Links.csv'), encoding='utf-8-sig', index=False)
        except:
            pass
    print(f'Total Category: {len(all_links)}')


def get_sub_category_link():
    print('=================== Getting Sub Category Link ===================')
    df = pd.read_csv("Category_Links.csv")
    links = df['links'].values
    print("Total Links: " + str(len(links)))
    l = 0
    for link in links:
        l += 1
        print(f'Getting Sub Category {l} out of {len(links)}')
        try:
            soup = BeautifulSoup(requests.get(link).content, 'lxml')
            lis = soup.find('div', {'id': 'subcats'}).find_all('li')
            for li in lis:
                try:
                    lins = li.find_all('a', {'class': 'cat_link'})
                    for lin in lins:
                        ll = 'https://www.wikihow.com' + lin['href']
                        new_link = {
                            'links': ll,
                        }
                        # print(link)
                        df = pd.DataFrame([new_link])
                        df.to_csv('Sub_Category_Links.csv', mode='a', header=not os.path.exists('Sub_Category_Links.csv'), encoding='utf-8-sig', index=False)
                except:
                    pass
        except:
            pass


def get_data():
    print('=================== Getting Data ===================')
    df = pd.read_csv("Sub_Category_Links.csv")
    links = df['links'].values
    print("Total Links: " + str(len(links)))
    l = 0
    for link in links:
        l += 1
        print(f'Getting Data {l} out of {len(links)}')
        d = 0
        while True:
            d += 1
            try:
                print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Page: {d}')
                soup = BeautifulSoup(requests.get(link + '?pg=' + str(d)).content, 'lxml')
                articles = soup.find('div', {'id': 'cat_all'}).find_all('a')
            except:
                break
            try:
                articles = soup.find('div', {'id': 'cat_all'}).find_all('a')
                for article in articles:
                    article_title = ''
                    article_description = ''
                    article_category = ''
                    try:
                        soup = BeautifulSoup(requests.get(article['href']).content, 'lxml')
                        try:
                            article_title = soup.find('h1', {'id': 'section_0'}).text
                        except:
                            pass
                        try:
                            temp = soup.find('div', {'id': 'mf-section-0'})
                            for div in temp.find_all('sup', {'class': 'reference'}):
                                div.decompose()
                            article_description = temp.text.replace('\n', '')
                            temps = soup.find('div', {'id': 'mf-section-1'}).find_all('div', {'class': 'step'})
                            cnt = 0
                            if len(temps) == 0:
                                temps = soup.find('div', {'id': 'mf-section-2'}).find_all('div', {'class': 'step'})
                            if len(temps) == 0:
                                temps = soup.find('div', {'id': 'steps'}).find_all('div', {'class': 'step'})
                            for temp in temps:
                                for div in temp.find_all('sup', {'class': 'reference'}):
                                    div.decompose()
                                for div in temp.find_all('div', {'class': 'mwimg'}):
                                    div.decompose()
                                cnt += 1
                                article_description += f'\n\n{cnt}\n' + temp.text.replace('\n', '')
                        except:
                            pass
                        try:
                            temps = soup.find('ul', {'id': 'breadcrumb'}).find_all('li')
                            for temp in temps:
                                article_category += temp.text + ' >> '
                        except:
                            pass
                    except:
                        pass
                    data = {
                        'URL': article['href'],
                        'Title': article_title,
                        'Category': article_category[:-3],
                        'Article': article_description.replace('\nX\nResearch source', '').replace('’', "'").replace(
                            "“", '"'),
                    }
                    # print(data)
                    df = pd.DataFrame([data])
                    df.to_csv(f'wikihow' + n + '.csv', mode='a', header=not os.path.exists(f'wikihow' + n + '.csv'), encoding='utf-8-sig', index=False)
            except:
                pass
    print("++++++++++++++++++++++++ Final Data Save +++++++++++++++++++++++++++++++")


if __name__ == '__main__':
    get_category_link()
    get_sub_category_link()
    get_data()
