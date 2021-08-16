#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# одновременное выполнение команд на множестве хостов

import subprocess
import sys, os, re
from multiprocessing.dummy import Pool
import getpass
import time
import paramiko
import curses

conf = {'host1'   :'name',
        'host2'   :1,
        'host3'   :3,
        'host4'   :'.domain.ru',
        'sudo'    :'n',
        'user'    :'toor',
        'password':'',
        'cmd'     :'',
        'show'    :'n',
        'allhosts':[],
        'hosts'   :[],
        'ssh_port':22,
        'out_cmd' :'n'
       }

mpool = {'poolstat':'ON',#ON/OFF
         'V_Pool':1
	    }       

pool = Pool(mpool['V_Pool'])

def out_red(text):
    print("\033[31m {}" .format(text))

def out_yellow(text):
    print("\033[33m {}" .format(text))

def out_blue(text):
    print("\033[36m {}" .format(text))

def out_green(text):
    print("\033[32m {}" .format(text))

def out_default(text):
    print("\033[37m\033[40m {}" .format(text))

def out_dane(text, new_line = False):
    if new_line == False:
        print("\033[30m\033[42m {}" .format(text), end = ' ')
    else:
        print("\033[30m\033[42m {}" .format(text), end = ' ')
        out_default('')

def out_error(text, new_line = False):
    if new_line == False:
        print("\033[37m\033[41m {}" .format(text), end = ' ')
    else:
        print("\033[37m\033[41m {}" .format(text), end = ' ')
        out_default('')

def decor1(text):
    out_yellow('\n\t\t\t'+text)
    print(' __________________________________________________________________________')

def decor2(text):
    out_yellow('\n\t\t\t'+text)

def decor2_1(text):
    out_yellow('\t\t\t'+text)

def decor3(text):
    out_default(' |__________________________________________________________________________')
    print('  |  ')
    array = text.split('\n')
    for line in array:
        print('  |  '+line)
    print('  |__________________________________________________________________________\n')

def test_connect(host):
    while True:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, username=conf['user'], password=conf['password'], port=conf['ssh_port'])
            stdin, stdout, stderr = client.exec_command('w')
            if stdout.channel.recv_exit_status() == 0:
                client.close()
                out_default('')
                break
        except:
            out_blue('')
            while True:
                try:
                    conf['password'] = getpass.getpass('  Пароль не верный попробуйте еще раз: ')
                    if conf['password']:
                        break
                except:
                    pass        

def run(host):
    command = conf['cmd']
    if conf['sudo'] == 'Y':
        command = 'echo '+conf['password']+'|sudo -S '+conf['cmd']

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=conf['user'], password=conf['password'], port=conf['ssh_port'])
    stdin, stdout, stderr = client.exec_command(command)
  	   
    if stdout.channel.recv_exit_status() == 0:
        out_green(' [OK]\t\t\t '+ host )
        if conf['out_cmd'] == 'Y':
            decor3(stdout.read().decode(encoding='utf-8'))
    else:    
        out_red(' [FAILED]\t\t '+ host )
        if conf['out_cmd'] == 'Y':
            decor3(stderr.read().decode(encoding='utf-8'))

    client.close()


def host_exist(host):  
    conf['hosts'].clear()
    if subprocess.call('nslookup '+host+' >> /dev/null', shell=True) == 0: 
        if subprocess.call("ping -c 1 " + host + ' >> /dev/null', shell=True) == 0:

            conf['hosts'].append(host)
            out_green('[OK]\t\t\t '+ host)
        else:
            out_red('[FAILED]\t\t '+ host + '\t\tis down')
    else:
        out_red('[FAILED]\t\t '+ host + '\t\tunknow host')  

def corect_input(text, str, default = None):
    while True:
        try:
            conf[str] = input(text)
            if conf[str]:
                break
            elif default:
            	conf[str] = default
            	break
        except:
            pass

def step1():
    decor1(' Удаленное выполнение команд')
    out_default('\n Пример нам надо выполнить команду на хостах \n с: host1.domain.ru \n по: host10.domain.ru')
    print(' Имя хоста до инкрементирующей части в примере это oper')
    print(' Начало инкремента получится = 3')
    print(' Окончания инкремента = 10')
    out_yellow(' __________________________________________________________________________')

    out_blue('')
    try:
        corect_input(' 1. Введите имя хоста до инкрементирующей части по умолчанию [ '+ conf['host1'] +' ]: ', 'host1', conf['host1'])
        corect_input(' 2. Введите цифру начала инкремента: ', 'host2')
        corect_input(' 3. Введите цифру окончания инкремента: ', 'host3')
        corect_input(' 4. Введите остальную часть домена по умолчанию [ '+ conf['host4'] +' ]: ', 'host4', conf['host4'])
        corect_input(' 5. Введите имя пользователя [ '+ conf['user'] +' ]: ', 'user', conf['user'])
        while True:
	        try:
	            conf['password'] = getpass.getpass(' 6. Введите пароль: ')
	            if conf['password']:
	                break
	        except:
	            pass
        corect_input(' 7. Надо ли повышать привилегии по умолчанию [ '+ conf['sudo'] +' ](Y/n): ', 'sudo', conf['sudo'])
        corect_input(' 8. Надо ли выводить вывод команд? [ '+ conf['out_cmd'] +' ](Y/n): ', 'out_cmd', conf['out_cmd'])
        corect_input(' 9. Введите команду которую хотите выполнить на удаленных хостах CMD: ', 'cmd')
        
    except:
        return 0
    return 1
    
def step2():
    decor1('Доступные хосты')
    print('')
    conf['allhosts'].clear()
    for i in range(int(conf['host2']), int(conf['host3'])+1):
        conf['allhosts'].append(conf['host1']+str(i)+conf['host4']) 

    curses.wrapper(draw_menu)
    step2_1()    

    while len(conf['allhosts']) != len(conf['hosts']):
        out_blue('')
        if input(' Доступны не все хосты, повторить проверку? [n](Y/n): ') == 'Y':
            curses.wrapper(draw_menu)
            out_default('\n')
            step2_1()
        else:
            out_default('')
            break
    return 1

def step2_1():
    if (mpool['poolstat'] == 'ON'):
        mpool['V_Pool'] = int(conf['host3']) - int(conf['host2'])+1
        pool = Pool(mpool['V_Pool'])
        pool.map(host_exist, conf['allhosts'])
    else:
        for host in conf['allhosts']:
            host_exist(host)


def step3():
    decor1('Выполнение на хостах')
    decor2('Всего хостов: '+ str(len(conf['allhosts'])))
    decor2_1('Доступных хостов: '+ str(len(conf['hosts'])))
    decor2_1('cmd = '+conf['cmd'])
    out_default('')

    start_time = time.time()

    if (mpool['poolstat'] == 'ON'):
        mpool['V_Pool'] = len(conf['hosts'])
        pool = Pool(mpool['V_Pool'])
        pool.map(run, conf['hosts'])
        decor2("--- %s Time ---" % (time.time() - start_time))
        return 1
    else:
        for host in conf['hosts']:
            run(host)
        decor2("Time: %s" % (time.time() - start_time))
        return 1
    return 0

def reppid():
    out_blue('')
    print('  Для выхода наберите exit | чтобы ввести новые данные введите new')
    corect_input('  Введите команду которую хотите выполнить на удаленных хостах CMD: ', 'cmd')       
    if conf['cmd'] == 'exit':
        exit()
    elif conf['cmd'] == 'new':
        new()
    else:
        step3()

def draw_menu(stdscr):
    step_up = 5
    flag = False
    hosts={}
    for host in conf['allhosts']:
        hosts[host] = True
    #print(hosts)

    k = 0
    cursor_x = 5
    cursor_y = 5

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    while (k != ord('q')):
        if k==10:
            flag = True
            break

        # Initialization
        stdscr.clear()

        height, width = stdscr.getmaxyx()

        if height <= len(conf['allhosts'])+step_up:
            flag = False
            break

        cursor_x = (width // 2 - ((len(conf['allhosts'][0])+4) // 2) - (len(conf['allhosts'][0])+4) % 2)+1

        title1 = "Вы можете указать игнорируемые хосты"
        title2 = "для выбора используйте пробел"

        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(2, int((width // 2) - (len(title1) // 2) - (len(title1) % 2)), title1)
        stdscr.addstr(3, int((width // 2) - (len(title2) // 2) - (len(title2) % 2)), title2)
        stdscr.attroff(curses.color_pair(4))

        for y in range(len(conf['allhosts'])):
            if hosts[conf['allhosts'][y]] == True:
                stdscr.attron(curses.color_pair(4))
                stdscr.addstr(step_up+y, int((width // 2) - ((len(conf['allhosts'][y])+4) // 2) - (len(conf['allhosts'][y])+4) % 2) , '[*] '+conf['allhosts'][y])
                stdscr.attroff(curses.color_pair(4))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(step_up+y, int((width // 2) - ((len(conf['allhosts'][y])+4) // 2) - (len(conf['allhosts'][y])+4) % 2) , '[ ] '+conf['allhosts'][y])
                stdscr.attroff(curses.color_pair(2))

        if k == 32:
            stdscr.clear()
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(2, int((width // 2) - (len(title1) // 2) - (len(title1) % 2)), title1)
            stdscr.addstr(3, int((width // 2) - (len(title2) // 2) - (len(title2) % 2)), title2)
            stdscr.attroff(curses.color_pair(4))
            if hosts[conf['allhosts'][cursor_y-step_up]] != False:
                hosts[conf['allhosts'][cursor_y-step_up]] = False
            else:
                hosts[conf['allhosts'][cursor_y-step_up]] = True
            for y in range(len(conf['allhosts'])):
                if hosts[conf['allhosts'][y]] == True:
                    stdscr.attron(curses.color_pair(4))
                    stdscr.addstr(step_up+y, int((width // 2) - ((len(conf['allhosts'][y])+4) // 2) - (len(conf['allhosts'][y])+4) % 2) , '[*] '+conf['allhosts'][y])
                    stdscr.attroff(curses.color_pair(4))
                else:
                    stdscr.attron(curses.color_pair(2))	
                    stdscr.addstr(step_up+y, int((width // 2) - ((len(conf['allhosts'][y])+4) // 2) - (len(conf['allhosts'][y])+4) % 2), '[ ] '+conf['allhosts'][y])
                    stdscr.attroff(curses.color_pair(2))                    
            cursor_y = cursor_y + 1
            stdscr.refresh()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(5, cursor_y)
        cursor_y = min(len(conf['allhosts'])+step_up-1, cursor_y)

        statusbarstr = "Press 'q' to exit | Press 'ENTER' to next step | Pos: {}, {}".format(cursor_x, cursor_y)
        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        stdscr.move(cursor_y, cursor_x)
        # Refresh the screen
        stdscr.refresh()
        # Wait for next input
        k = stdscr.getch()

    if flag == True:
        for k, v in hosts.items():
    	    if v == False:
    	        conf['allhosts'].remove(k)

def new():
    if step1():
        if step2():
            test_connect(conf['hosts'][0])
            if step3():
                while True:
                    if conf['cmd'] != 'exit':
                        reppid()
                    else:
                        break

if __name__ == '__main__':
    new()
    out_default('')
    pool.close()
    pool.join()
    
