#!/usr/bin/python3
import time
import pickle
import random
import requests
import os.path
from datetime import datetime
from multiprocessing import Pool
import re

############################################# параметры парсинга ###########################################################
sub_url = 'http://'             #добавляется перед адресом сайта

sleep_status = 'OFF'            #ON/OFF - включает задержку между запросами 
stb = 3                         #минимальное время задержки между переходами
ste = 15                        #максимально время зажержки между переходами

pool_status = 'ON'              #ON/OFF включает мультипоточность
V_Pool = 20                     #количество потоков


PATH_SITE = 'site'
PATH_EMAIL = 'emails'
PATH_EMAIL_END = 'emails_no_repit'
PATH_COMPLITED = 'complited'


site = []
complited = []
emails = []

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

contacts = [
    '',
    '/contacts/',
    '/kontakty',
    '/kontaktyi/'
]


def new_headers():
    new_headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.8,en;q=0.6',
            'Connection':'keep-alive',
            'Origin':'https://yandex.ru',
            'Upgrade-Insecure-Requests':'1',
            }
    new_headers['User-Agent'] = random.choice( user_agent_list )

    return new_headers



def get_html(url, theaders):
    msleep()
    try:
        r = requests.get(url, headers = theaders)
    except:
        r = requests.get( 'http://site.ru' , headers = theaders)
    return r.text

def msleep():
    if (sleep_status == 'ON'):
        time.sleep( random.randint(stb,ste) )



def find_mail(url):

    if not complited:

        for contact in contacts:
            html_txt = get_html( sub_url + url + contact, new_headers() )
            emails = re.findall(r'[\w.-]+@[\w.-]+\.?[\w]+?', html_txt)
            print('#################################################')
            print('сайт http://' + url + contact)
            try:
                for email in emails:
                    print('##### ' + email)
                    save_add(PATH_EMAIL, email)
            except:
                print('not email ' + sub_url + url + contact )

        save_add(PATH_COMPLITED, url)

    else:

        inf_complited = 0

        for line in complited:
            if line == url:
                inf_complited = 1

        if inf_complited != 1:

            for contact in contacts:
                html_txt = get_html( sub_url + url + contact, new_headers() )
                emails = re.findall(r'[\w.-]+@[\w.-]+\.?[\w]+?', html_txt)
                print('#################################################')
                print('сайт http://' + url + contact)
                try:
                    for email in emails:
                        print('##### ' + email)
                        save_add(PATH_EMAIL, email)
                except:
                    print('not email ' + sub_url + url + contact )

            save_add(PATH_COMPLITED, url)

        else:
            print('is complited ' + url)



def save_links(PATH, links):
    with open(PATH, "w") as f:
        for i in links:
            f.write(str(i) + "\n")

def save_add(PATH, email):
    with open(PATH, "a") as f:
        f.write(email + "\n")

def read_links(PATH, links):
    links.clear()
    with open(PATH, "r") as f:
        for line in f:
            try:
                links.append(line.strip())
            except:
                print('file ' + PATH + ' do\'nt load ' + line)



def main():
    start = datetime.now()

    print('#################################################')

    if (os.path.exists(PATH_SITE)):
        read_links(PATH_SITE, site)
        print('file '+ PATH_SITE +' exest')
    else:
        print('file '+ PATH_SITE +' not exest')

    if (os.path.exists(PATH_COMPLITED)):
        read_links(PATH_COMPLITED, complited)
        print('file '+ PATH_COMPLITED +' exest')
    else:
        print('file '+ PATH_COMPLITED +' not exest')

    if (os.path.exists(PATH_EMAIL)):
        read_links(PATH_EMAIL, emails)
        emails_new = list(set(emails))
        save_links(PATH_EMAIL_END, emails_new)


    print('#################################################')


    if (os.path.exists(PATH_SITE)):

        if (pool_status == 'ON'):
            with Pool(V_Pool) as p:
             p.map(find_mail, site)
        else:
            for url in site:
                find_mail(url)

    else:
        print('file '+ PATH_SITE +' not exest, end parsing')

    print('#################################################')

    end = datetime.now()

    total = end - start
    print('Вреся выполнения парсинга = ' + str( total ))

if __name__ == '__main__':
    main()











