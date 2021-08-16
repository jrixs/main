#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import configparser
import smtplib                                      
import socket
import os
from email.mime.multipart import MIMEMultipart      
from email.mime.text import MIMEText                
import datetime

now = datetime.datetime.now()         
smtp_configure = '/opt/usbscanner_0.1/smtp.conf'
PATH_USB_DEV = '/opt/usbscanner_0.1/usb.csv'
hostname = socket.gethostbyaddr(socket.gethostbyname('docker1'))[0]
zone = hostname[hostname.find(".")+1:].split(".")[0]

tmp = []
usb_device_list = []
usb_device_list_id = []
mail = []
USB = {}
USB_BAK = {}

def SMTP_CONF(conf_file, block, value):
    try:
        parser = configparser.RawConfigParser()
        parser.read(conf_file)
        config_tmp = dict(parser.items(block))
    except:
        mail.append('not file: '+smtp_configure)
        exit
    return config_tmp[value]

def send_mail(USB):
    msg = MIMEMultipart()                          
    msg['From']    = SMTP_CONF(smtp_configure, 'smtp-config', 'addr_from')
    msg['To']      = SMTP_CONF(smtp_configure, 'smtp-config', 'addr_to')
    msg['Subject'] = zone + ' Изменение конфигурации ' + zone +' ' + socket.gethostname()

    body = now.strftime("%d-%m-%Y %H:%M") + " " + socket.gethostname()
    msg.attach(MIMEText(body, 'plain'))
    
    for event in mail:
        msg.attach(MIMEText(event, 'html', 'utf-8'))

    msg.attach(MIMEText('\nТекущая конфигурация', 'html', 'utf-8'))
    for key in USB:
        msg.attach(MIMEText('Name: '+key+'\t'+'S/N: '+USB[key], 'html', 'utf-8'))

    server = smtplib.SMTP(SMTP_CONF(smtp_configure, 'smtp-config', 'smtp_server'), SMTP_CONF(smtp_configure, 'smtp-config', 'smtp_port'))
    try:
        server.login(SMTP_CONF(smtp_configure, 'smtp-config', 'addr_from'), SMTP_CONF(smtp_configure, 'smtp-config', 'password'))
        server.send_message(msg)
    except:
        mail.append('Не удалось подключится проверьте актуальность данных в файле '+smtp_configure)
    server.quit()

def sell_cmd(cmd, arg):
    usb_device_list = []
    usb_device_list_dev = subprocess.run([cmd, arg], stdout=subprocess.PIPE)
    for usb_device in usb_device_list_dev.stdout.decode('utf8').split('\n'):
        usb_device_list.append(usb_device)
    return usb_device_list

def sell_cmd1(cmd, arg1, arg2, arg3):
    usb_device_list_dev = subprocess.run([cmd, arg1, arg2, arg3], stdout=subprocess.PIPE)
    return usb_device_list_dev.stdout.decode('utf8')

def sell_cmd2(cmd, arg1, arg2, arg3):
    usb = []
    out = subprocess.run([cmd, arg1, arg2, arg3], stdout=subprocess.PIPE)
    for usb_device in out.stdout.decode('utf8').split('\n'):
        usb.append(usb_device)
    return usb

def parcer_2(sstring):
    return sstring[sstring.find("\"")+1:].split("\"")[0]

def wrait_usb_list(USB):
    with open(PATH_USB_DEV, "w") as f:
        f.write("")
    for key in USB:
        with open(PATH_USB_DEV, "a") as f:
            f.write(key+";"+USB[key] + "\n")

def read_usb_list():
    if PATH_USB_DEV:
        try:
            with open(PATH_USB_DEV) as File:
                for row in File:
                    USB_BAK[row[0:].split(';')[0]] = row[row.find(";")+1:].split('\n')[0]
            return 1
        except:
            wrait_log('file: '+PATH_USB_DEV+' is bad')
            return 0

def verify_usb():
    send_status = 0
    for key in USB:
        if key in USB_BAK:
            if USB[key] != USB_BAK[key]:
                mail.append('Изменилось устройство: '+key+' S/N был: \t\t\t'+USB_BAK[key]+' S/N стал: \t\t\t'+USB[key]+'\n')
                send_status = 1
        else:
            mail.append('Найдено новое устройство: \t'+key+'\nS/N: \t\t\t'+USB[key]+'\n')
            send_status = 1
    for key in USB_BAK:
        if key in USB:
            pass
        else:
            mail.append('Пропало устройство: \t'+key+'\nS/N: \t\t\t'+USB_BAK[key])
            send_status = 1
    if send_status:
        send_mail(USB)

def wrait_log(lines):
    log = open(SMTP_CONF(smtp_configure, 'smtp-config', 'path_log'), 'a')
    for text in lines:
        log.write(str(time.strftime("%d %m %H:%M:%S", time.localtime())) + '\t' + text + '\n')
    log.close()


os.system('touch '+PATH_USB_DEV)
usb_device_list = sell_cmd('ls', '/dev/input/by-id/')
for r1 in usb_device_list:
    if r1 !='':
        tmp.append(sell_cmd1('udevadm', 'info', '--query=path', '--name=/dev/input/by-id/'+r1))

usb_device_list_id = [line.rstrip() for line in tmp]

for r2 in usb_device_list_id:
    key = ''
    value = ''
    for r3 in sell_cmd2('udevadm', 'info', '--attribute-walk', '--path='+r2):
        if 'ATTRS{name}' in r3:
            key = parcer_2(r3)
        if 'ATTRS{uniq}' in r3:
            value = parcer_2(r3)
    USB[key] = value

if read_usb_list():
    verify_usb()
if mail:
    wrait_log(mail)

wrait_usb_list(USB)

os.system('sed -i /$usbscanner.py/d /var/spool/cron/crontabs/root')
