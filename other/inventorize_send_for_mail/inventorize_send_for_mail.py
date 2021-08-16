#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pickle
import time

os.system('pip3 install --upgrade '
          'print-function '
          'google-api-python-client '
          'google-auth-httplib2 '
          'google-auth-oauthlib '
          '--user requests')

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
BED_LIST = []
PROJECT_LIST = []
info_mail = []

smtp_server = ''
smtp_port = '587'
addr_from = ''
password = ''

now = datetime.datetime.now()

def get_tab(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME, CREDENTIALS = 'credentials.json', TOKEN = '/opt/inventory_to_mail/token.pickle'):
    creds = None
    if os.path.exists(TOKEN):
        with open(TOKEN, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        return []
    else:
        return values


def send_mail(LIST, PROJECT='',TO='it@mail.ru'):
    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = TO
    msg['Subject'] = PROJECT + ' ЗАДОЛЖНОСТЬ на ' + now.strftime("%d-%m-%Y %H:%M")

    msg.attach(MIMEText('\nСписок сотрудников за которыми числится оборудование актуален на ' + now.strftime("%d-%m-%Y %H:%M"), 'html', 'utf-8'))
    if not LIST:
        return 1
    else:
        msg.attach(MIMEText('<table border = \"1\" cellpadding = \"0\" cellspacing = \"0\" width = \"100%\">'
                            '<tr>'
                            '<th width = \"100px\" text-align=\"center\"> Дата </th>'
                            '<th width = \"40px\"  text-align=\"center\"> № </th>'
                            '<th width = \"300px\" text-align=\"center\"> ФИО </th>'
                            '<th width = \"500px\" text-align=\"center\"> Оборудование </th>', 'html', 'utf-8'))

        for key in LIST:
            msg.attach(MIMEText('<table border = \"1\" cellpadding = \"0\" cellspacing = \"0\" width = \"100%\">'
                                '<tr>'
                                '<td width = \"100px\" text-align=\"center\";>'+key[0]+
                                '</td><td width = \"40px\" text-align=\"center\">'+key[1]+
                                '</td><td width = \"300px\" text-align=\"center\">'+key[2]+
                                '</td><td width = \"500px\" text-align=\"center\">'+key[4]+'</td>', 'html', 'utf-8'))

    msg.attach(MIMEText('\nЭтот отчет составлен автоматически и служит для осведомленности сотрудников не отвечайте на это письмо.\nСпасибо!','html', 'utf-8'))

    server = smtplib.SMTP(smtp_server,smtp_port)
    try:
        server.login(addr_from, password)
        server.send_message(msg)
        print(now.strftime("%d-%m-%Y %H:%M") + ' send mail')
    except:
        print(now.strftime("%d-%m-%Y %H:%M") + ' error: mail not send')
    server.quit()

if __name__ == '__main__':
    LIST = get_tab('1SXNZIb45nWN_KoCGOkStG51xCp81b7PXlYxLJdexniM','Sheet1!A2:H')
    info_mail = get_tab('1SXNZIb45nWN_KoCGOkStG51xCp81b7PXlYxLJdexniM','info_mail!B2:C')

    for row in LIST:
        if row[-1] != "возврат":
            BED_LIST.append(row)

    for row1 in info_mail:
        temp_list = []
        for row2 in BED_LIST:
            if not row1[0]:
                print('error')
            elif row1[0] == row2[3]:
                temp_list.append(row2)
        send_mail(temp_list, row1[0], row1[1])
        time.sleep(15)
