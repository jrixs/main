#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import pickle
import random
import requests
#import csv
import json
import os.path
from datetime import datetime
from bs4 import BeautifulSoup
from multiprocessing import Pool
from itertools import groupby
from splinter import Browser

############################################# параметры парсинга ###########################################################
url = ''                                                                                    #начальная страница для парсинга
PATH_SUB_URL = ''                                                                           #для того чтобы сделать из относительных ссылок абсолютные

sleep_status = 'ON'                                                                         #ON/OFF - включает задержку между запросами
stb = 7                                                                                     #минимальное время задержки между переходами
ste = 23                                                                                    #максимально время зажержки между переходами

list2_scan = 'ON'                                                                           #ON/OFF - включат парсинг ссылок в виде картинок

PATH_DATA = 'data.csv'                                                                      #путь к выгружаемому файлу

links1 = []
links2 = []
links_bak2 = []
links3 = []
links_bak3 = []
nav_links = []
links3complid = []
linksdatacomplid = []
DATA = []

PATH_LINKS_1LVL = 'links1'
PATH_LINKS_2LVL = 'links2'
PATH_LINKS_2LVL_BAK = 'links2bak'
PATH_LINKS_3LVL = 'links3'
#PATH_LINKS_NAV_3_LVL = 'links3nav'
PATH_LINKS_COMPLID_3LVL = 'links3complid'
PATH_LINKS_COMPLID_DATA = 'LinksDataComplid'
PATH_LOG = 'seti.log'


browser = Browser(
    executable_path='/usr/share/mail_proekt/geckodriver',
    log_path='/usr/share/mail_proekt/geckodriver.log',
    firefox_binary='/usr/bin/firefox'
    )

def new_headers(url_bak):
    new_headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'site.ru',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
            }
    new_headers['Referer'] = url_bak
    return new_headers



def get_html(url, theaders):
    r = requests.get(url, headers=theaders)
    return r.text

def mprint(line):
    now = datetime.now()
    print(now.strftime("%d-%m-%Y %H:%M:%S")  + ' | ' + line)
    line_log = now.strftime("%d-%m-%Y %H:%M:%S") + ' | ' + line
    save_add(PATH_LOG, line_log)

def get_all_links_1lvl(html):
    soup = BeautifulSoup(html, 'lxml')
    #mprint("################################## html ###########################################")
    #mprint(html) 
    #mprint("###################################################################################")

    tds =  soup.find_all('div', class_='iconRubric')

    for td in tds:
        try:
            a = td.find('a', class_='iconRubric__link').get('href')
            link = PATH_SUB_URL + a
            links1.append(link)
            mprint('Группа ' + link )
        except:
            mprint('Групп не найдено')

    save_links(PATH_LINKS_1LVL, links1)


def get_all_links_2lvl( all_links_1lvl ):
    
    links2.clear()
    links_bak2.clear()

    for murl in all_links_1lvl:
        msleep()

        temp = get_html( murl, new_headers( url ))

        soup1 = BeautifulSoup( temp, 'lxml')
        mprint('##########################################################')
        mprint('######' + murl)

        tds1 = soup1.find_all('div', class_='moreRubric')
        for td in tds1:
            try:
                a = td.find('a', class_='link moreRubric__caption').get('href')
                link = PATH_SUB_URL + a
                links2.append( link )
                links_bak2.append( murl )
                mprint('Подгруппа 1 вариант = ' + link )
            except:
                mprint('Подгруппа 1 вариант не найдены')

        if list2_scan == 'ON':
            soup2 = BeautifulSoup( temp, 'lxml')
            tds2 = soup2.find_all('div', class_='iconRubric')
            for td in tds2:
                try:
                    a = td.find('a', class_='link iconRubric__link').get('href')
                    link = PATH_SUB_URL + a
                    links2.append( link )
                    links_bak2.append( murl )
                    mprint('Подгруппа 2 вариант = ' + link )
                except:
                    mprint('Подгруппа 2 вариант не найдены')


    save_links(PATH_LINKS_2LVL, links2)
    save_links(PATH_LINKS_2LVL_BAK, links_bak2)



def save_links(PATH, links):
    with open(PATH, "w") as f:
        for i in links:
            f.write(str(i) + "\n")

def save_add(PATH, line):
    with open(PATH, "a") as f:
        f.write(line + "\n")


def read_links(PATH, links):
    links.clear()
    with open(PATH, "r") as f:
        for line in f:
            try:
                links.append(line.strip())
            except:
                mprint('файл ' + PATH + ' не загрузил' + line)
                 

def get_links_3lvl():
    link = ''
    nav_links.clear()
    msleep()

    test = browser.html

    #print("################### " + url)
    #print(test) 
    #print("###################################################################################")
    soup1 = BeautifulSoup( test, 'lxml')                                    
    tds1 = soup1.find_all('h3', class_='miniCard__headerTitle')

    try:
        for td1 in tds1:   
            a = td1.find('a', class_='miniCard__headerTitleLink').get('href')
            link = PATH_SUB_URL + a
            links3.append(link)
            save_add(PATH_LINKS_3LVL, link)
            mprint('карточка организации 1 вариант = ' + link)
    except:
        mprint('карточки организаций по 1 варианту не найдены')


    soup2 = BeautifulSoup( test, 'lxml')
    tds2 = soup2.find_all('article', class_='mediaMiniCard')

    try:
        for td2 in tds2:
            a = td2.find('a', class_='mediaMiniCard__link').get('href')
            link = PATH_SUB_URL + a
            links3.append(link)
            save_add(PATH_LINKS_3LVL, link)
            mprint('карточка организации 2 вариант = ' + link)
    except:
        mprint('карточки организаций по 2 варианту не найдены')   
    

def get_all_links_3lvl():
    
    COMPLITED = 0

    for i in range( len(links2) ):

        mprint('###############################################################################')
        mprint( links2[i] )

        if (os.path.exists(PATH_LINKS_COMPLID_3LVL)):
            read_links(PATH_LINKS_COMPLID_3LVL, links3complid)
            #print('file links3 complid read')

            for j in range( len( links3complid ) ):

                if links3complid[j] == links2[i]:
                    mprint('COMPLITED' ) # + links2[i])
                    COMPLITED = 1

            if COMPLITED != 1:
                browser.visit( links2[i] )
                get_links_3lvl()
                try:
                    elems = browser.find_by_css('div[class="pagination__arrow _right"]')
                    while len(elems) == 1:
                        elems.click()
                        mprint('next page exists')
                        get_links_3lvl()
                        #elems = browser.find_by_css('div[class="pagination__arrow _right"]')
                except:
                    pass

                save_add(PATH_LINKS_COMPLID_3LVL, links2[i])
                    
        
        else:

            browser.visit( links2[i] )
            get_links_3lvl()
            try:
                elems = browser.find_by_css('div[class="pagination__arrow _right"]')
                while len(elems) == 1:
                    elems.click()
                    mprint('next page exists')
                    get_links_3lvl()
                    #elems = browser.find_by_css('div[class="pagination__arrow _right"]')
            except:
                pass

            save_add(PATH_LINKS_COMPLID_3LVL, links2[i])

        COMPLITED = 0



def get_data():

    for i in range( len(links3) ):

        COMPLITED = 0

        mprint('###############################################################################')
        mprint( links3[i] )    
        
        if (os.path.exists(PATH_LINKS_COMPLID_DATA)):
            read_links(PATH_LINKS_COMPLID_DATA, linksdatacomplid)

            for j in range( len(linksdatacomplid) ):
                if links3[i] == linksdatacomplid[j]:
                    mprint( 'COMPLITED' )
                    COMPLITED = 1
        
        if COMPLITED != 1:

            browser.visit( links3[i] )

            time.sleep(1)

            try:
                elems = browser.find_by_css('div[class="contact__phonesFadeShow"]')
                while len(elems) == 1:
                    elems.click()
                    #print('телефон раскрыт 1 вариант')
            except:
                pass

            try:
                elems = browser.find_by_css('span[class="mediaContacts__showPhones"]')
                while len(elems) == 1:
                    elems.click()
                    #print('телефон раскрыт 2 вариант')
            except:
                pass

            test = browser.html

            soup = BeautifulSoup( test, 'lxml')


            #Вариант 1
            #Название
            #div cardHeader__headerName
            #h1 cardHeader__headerNameText
            #
            #Телефон
            #div contact__phonesFadeShow - нажать
            #div contact__phonesItem _type_phone
            #a contact__phonesItemLink
            #
            #сайт
            #div contact__link _type_website
            #a link contact__linkText
            #
            #Почта
            #header contact__otherHeader - нажать(ненужно)
            #div contact__link _type_email
            #a link contact__linkText

            d1_name = 'none'
            d1_tel = ''
            d1_web = 'none'
            d1_email = 'none'

            try:
                d1_name = soup.find('h1', class_='cardHeader__headerNameText').text.strip()
            except: 
                pass
                #mprint('Вариант 1 Название не найдено')

            
            all1_tel = soup.find_all('div', class_='contact__phonesItem _type_phone')
            for n_tel in all1_tel:
                try:
                    tel = n_tel.find('a',class_='contact__phonesItemLink').get('href')
                    d1_tel += tel + ' '
                except:
                    pass
                    #mprint('Вариант 1 телефон не найден')

            web1 = soup.find('div', class_='contact__link _type_website')
            try:
                d1_web = web1.find('a', class_='link contact__linkText').text
            except:
                pass
                #mprint('Вариант 1 сайт не найден')


            email1 = soup.find('div', class_='contact__link _type_email')
            try:
                d1_email = email1.find('a', class_='link contact__linkText').text.strip()
            except:
                pass
                #mprint('Вариант 1 email не найден')

            
            #Вариант 2
            #Название 
            #div mediaCardHeader__cardHeader
            #h1 mediaCardHeader__cardHeaderName
            #
            #Телефон
            #span mediaContacts__showPhones - нажать
            #span mediaContacts__phonesItemCut
            #a mediaContacts__phonesNumber
            #
            #Сайт
            #li mediaContacts__groupItem _website
            #a mediaContacts__item mediaContacts__website
            #
            #Почта
            #li mediaContacts__groupItem _email
            #a mediaContacts__item mediaContacts__email

            d2_name = 'none'
            d2_tel = ''
            d2_web = 'none'
            d2_email = 'none'

            try:
                d2_name = soup.find('h1', class_='mediaCardHeader__cardHeaderName').text.strip()
            except:
                pass
                #mprint('Вариант 2 название не найдено')

            d2_tel = ''
            all2_tel = soup.find_all('span', class_='mediaContacts__phonesItemCut')
            for n_tel in all2_tel:
                try:
                    tel = n_tel.find('a',class_='mediaContacts__phonesNumber').get('href')
                    d2_tel += tel + ' '
                except:
                    pass
                    #mprint('Вариант 2 телефон не найден')

            web2 = soup.find('li', class_='mediaContacts__groupItem _website')
            try:
                d2_web = web2.find('a', class_='mediaContacts__item mediaContacts__website').text.strip()
            except:
                pass
                #mprint('Вариант 2 сайт не найден')

            email2 = soup.find('li', class_='mediaContacts__groupItem _email')
            try:
                d2_email = email2.find('a', class_='mediaContacts__item mediaContacts__email').text.strip()
            except:
                pass

            if d1_tel == '':
                d1_tel = 'none'
            if d2_tel == '':
                d2_tel = 'none'

            if d1_name != 'none':
                data = d1_name + ';' + del4char(d1_tel) + ';' + d1_web + ';' + d1_email
                save_add( PATH_DATA, data )
                mprint('Вариант 1 | ' + d1_name + ' | ' + del4char(d1_tel) + ' | ' + d1_web + ' | ' + d1_email )
            else:
                data = d2_name + ';' + del4char(d2_tel) + ';' + d2_web + ';' + d2_email
                save_add( PATH_DATA, data )
                mprint('Вариант 2 | ' + d2_name + ' | ' + del4char(d2_tel) + ' | ' + d2_web + ' | ' + d2_email )

            save_add(PATH_LINKS_COMPLID_DATA, links3[i])

            msleep()

        
def del4char(line):
    line = line.replace('tel:','')
    return line


def find_a(teg, p_class):
    for td in tds:
        a = td.find( teg, class_=p_class ).get('href')
        link = PATH_SUB_URL + a
        links3.append(link)
        mprint('Найденый элемент = ' + link)


def msleep():
    if (sleep_status == 'ON'):
        time.sleep( random.randint(stb,ste) )


def main():
    start = datetime.now()

    mheaders = new_headers( PATH_SUB_URL )


    if (os.path.exists(PATH_LINKS_1LVL)):
        read_links(PATH_LINKS_1LVL, links1)
        mprint('file links1 read')
    else:
        mprint('links 1 lvl parsing...')
        get_all_links_1lvl( get_html(url, mheaders) )


    if (os.path.exists(PATH_LINKS_2LVL)):
        read_links(PATH_LINKS_2LVL, links2)
        read_links(PATH_LINKS_2LVL_BAK, links_bak2)
        mprint('file links2 read')
        #get_all_links_2lvl( links1 )
    else:
        mprint('links 2 lvl parsing...')
        get_all_links_2lvl( links1 )


    if (os.path.exists(PATH_LINKS_3LVL)):
        read_links(PATH_LINKS_3LVL, links3)
        mprint('file links3 read')
        ###if (os.path.exists(PATH_LINKS_COMPLID_3LVL)):
        ###    read_links(PATH_LINKS_COMPLID_3LVL, links3complid)
        ###    print('file links3 complid read')
        get_all_links_3lvl()
    else:
        mprint('links 3 lvl parsing...')
        get_all_links_3lvl()


    if (os.path.exists(PATH_LINKS_COMPLID_DATA)):
        read_links(PATH_LINKS_COMPLID_DATA, linksdatacomplid)
        mprint('file ' + PATH_LINKS_COMPLID_DATA + ' read')
        get_data()
    else:
        mprint('get data...')
        get_data()
    #'span'mediaContacts__showPhones    

    
    browser.quit()

    end = datetime.now()

    total = end - start
    mprint(str(total))

    mprint("парсер выполнился")





















if __name__ == '__main__':
    main()


