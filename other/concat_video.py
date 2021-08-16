#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#============================================================
# склейка множество видео файлов в один файл с помощью ffmpeg
#============================================================

import glob
import subprocess
import os

conf = {'find_fales': '/tmp/20210711222000-20210711224500/*.mp4',   # обязательный параметр указывается каталог и файлы для склейки
        'del_text': 'IP ',                       # не обязательный параметр используется если надо удалить часть имени файла 
        'list': '/tmp/list.txt',      # обязательный параметр путь и место расположения списка для склейки
        'out_file':'/tmp/11_07_2021.mp4'  # обязательный параметр указывает путь и название готового файла
       }

def rename():
    if os.path.exists(conf['list']):
        return 0

    files_tmp = glob.glob( conf['find_fales'] )

    for i in files_tmp:
        if os.rename(i, i.replace(conf['del_text'], '' ) ):
	        print( 'rename ' +i+ ' failed!' )
        else:
            print( 'rename ' +i+ ' to '+ i.replace(conf['del_text'], '' ) )
    return 1

def set_list():
    files_tmp = glob.glob( conf['find_fales'] )
    file = open(conf['list'], 'w')
    for i in files_tmp:
        file.write(str('file \''+i+'\'\n'))
    file.close()
    return 1

def sum_mp4():
    if not os.path.exists(conf['list']):
    	return 0

    cmd = 'ffmpeg -f concat -safe 0 -i '+ conf['list'] +' -c copy '+ conf['out_file']
    if subprocess.call(cmd, shell=True) == 0:
    	print('\nConvert done!\nYou file: '+conf['out_file'])
    else:
    	print('Convert failed!')
    return 1

#Если файлы надо переименовать
if rename():
    if set_list():
        sum_mp4()
else:
    sum_mp4()

# Если файлы не надо переименовать
# Как выяснилось список можно создавать с абсолютным путем к файлу вместе
# с пробелами, функция переименования файлов не нужна но оставлена на всякий случай
#if set_list():
#    sum_mp4()
