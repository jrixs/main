#!/usr/bin/python3
import time
import pickle
import random
import requests
import os.path
from datetime import datetime
from bs4 import BeautifulSoup
#from multiprocessing import Pool
#import fake_useragent
import re

############################################# параметры парсинга ###########################################################
url = 'http://site.ru/'         #начальная страница для парсинга
stb = 3                         #минимальное время задержки между переходами
ste = 15                                                                                    #максимально время зажержки между переходами
PATH_CSV = 'test.csv'                                                                       #путь к выгружаемому файлу
links1 = []
links2 = []
links_bak2 = []
links3 = []
links_bak3 = []
email = []
PATH_EMAIL = 'email_kurskjspravru'
PATH_LINKS_1LVL = 'links1_js'
PATH_LINKS_2LVL = 'links2_js'
PATH_LINKS_2LVL_BAK = 'links2bak_js'
PATH_LINKS_3LVL = 'links3_js'
PATH_LINKS_3LVL_BAK = 'links3bak_js'
#test = ''
#XRequestId = '6a52f615-5b4f-12f0-a10f-127d08b0d52a'

user_agent_list = [
    #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

def new_headers(url_bak):
    new_headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.8,en;q=0.6',
            'Connection':'keep-alive',
            'Origin':'https://site.ru',
            'Upgrade-Insecure-Requests':'1',
            }
    new_headers['User-Agent'] = random.choice( user_agent_list )
    new_headers['Referer'] = url_bak
#    new_headers['X-Request-Id'] = XRequestId
    return new_headers



def get_html(url, theaders):
    r = requests.get(url, headers=theaders)
    return r.text


def get_all_links_1lvl(html):
    soup = BeautifulSoup(html, 'lxml')
    #print("################################## html ###########################################")
    #print(html) 
    #soup1 = BeautifulSoup(''.join(html))
    #print(tempe.prettify())
    #print("###################################################################################")

    tds =  soup.find_all('h3')

    for td in tds:
        a = td.find('a').get('href')
        link = 'http://site.ru' + a
        links1.append(link)

    save_links(PATH_LINKS_1LVL, links1)

    #return links


def get_all_links_2lvl( all_links_1lvl ):
    
    links2.clear()
    links_bak2.clear()
    link = ''

    for murl in all_links_1lvl:
        print('#####################' + murl + '#######################') 
        msleep()

        soup = BeautifulSoup( get_html( murl, new_headers( url ) ), 'lxml')
        
        tds = soup.find_all('div', class_='cat-item')

        for td in tds:
            a = td.find('a').get('href')
            link = 'http://site.ru' + a
            links2.append( link )
            links_bak2.append( murl )
            print(link)

    save_links(PATH_LINKS_2LVL, links2)
    save_links(PATH_LINKS_2LVL_BAK, links_bak2)
    #return links

def save_links(PATH, links):
    with open(PATH, "w") as f:
        for i in links:
            f.write(str(i) + "\n")
    
def read_links(PATH, links):
    links.clear()
    with open(PATH, "r") as f:
        for line in f:
            try:
                links.append(line.strip())
            except:
                print('файл ' + PATH + ' не загрузил' + line)
                 

def get_all_links_3lvl():
    
    link = ''

    for i in range(len(links2)):
        #msleep()

        print(links2[i] + ' тут ' + links_bak2[i])    
        print( new_headers( links_bak2[i] ) )
        
        test = get_html( links2[i], new_headers( links_bak2[i] ))
        #test = get_html( links2[i], headers={'User-Agent': UserAgent().chrome} )
        print("################################## html ###########################################")
        print(test) 
        print("###################################################################################")
        soup = BeautifulSoup( test, 'lxml')


        #soup = BeautifulSoup( get_html( links2[i], new_headers( links_bak2[i] ) ), 'lxml')
                                    
        tds = soup.find_all('h3', class_='miniCard__headerTitle')

        for td in tds:
            a = td.find('a', class_='link miniCard__headerTitleLink').get('href')
            link = 'https://site.ru' + a
            links3.append(link)
            links_bak3.append(links2[i])
            #проверка на бан если бана нету и ссфлка спарсилась удалить из ссылку с 2 списка

        print('Страница = ' + links2[i] + ' ССЫЛКА = ' + link)

        msleep()

    save_links(PATH_LINKS_3LVL, links3)
    save_links(PATH_LINKS_3LVL_BAK, links_bak3)

    #return links

def get_all_links_3lvl_old( html ):
    print("################################## html 3 lvl #####################################")
    print(html) 
    print("###################################################################################")
    links = []

    soup = BeautifulSoup( html, 'lxml')
            
    tds = soup.find_all('h3', class_='miniCard__headerTitle')
    
    for td in tds:
        a = td.find('a', class_='link miniCard__headerTitleLink').get('href')
        link = 'https://site.ru' + a
        links.append(link)

    return links


def msleep():
    time.sleep( random.randint(stb,ste) )
    

def write_csv(data):
    with open('temp.csv', 'a') as f:
        writer = csv.writer(f)
        for line in data:
            writer.writerow(line)


def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


def main():
    start = datetime.now()

    mheaders = new_headers( 'https://site.ru' )
    
    if (os.path.exists(PATH_LINKS_1LVL)):
        read_links(PATH_LINKS_1LVL, links1)
        print('file links1 exest')
    else:
        print('links 1 lvl parsing...')
        get_all_links_1lvl( get_html(url, mheaders) )





    if (os.path.exists(PATH_LINKS_2LVL)):
        read_links(PATH_LINKS_2LVL, links2)
        read_links(PATH_LINKS_2LVL_BAK, links_bak2)
        print('file links2 exest')
    else:
        print('links 2 lvl parsing...')
        get_all_links_2lvl( links1 )





    #if (os.path.exists(PATH_LINKS_3LVL)):
    #    read_links(PATH_LINKS_3LVL, links3)
    #    read_links(PATH_LINKS_3LVL_BAK, links_bak3)
    #    print('file links3 exest')
    #else:
    #    print('links 3 lvl')
    #    get_all_links_3lvl()


    #for url_2lvl in all_links_2lvl:
    #    msleep()
    #    list_link = get_all_links_3lvl( get_html(url_2lvl) )
    #    write_csv(list_link)
    #    print('спарсился ' + url_2lvl)
    
    end = datetime.now()

    total = end - start
    print(str(total))

    #print("парсер выполнился")





















if __name__ == '__main__':
    #print("точка входа")
    main()
#надо выводить двумерный список ссылка откуда был запрос и куда

