#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, time, sys
import pymysql
import datetime
from pymysql.cursors import DictCursor


path = '/record'
log_file = '/var/log/opvideo.log'

# MySQL params
config_sql_server = ['',                      #'server'
                     '',                      #'user'
                     '',                      #'password'
                     '',                      #'schema'
                     'utf8'                   #'encoding'
                     ]


def wrait_log(text):
  log = open(log_file, 'a')
  log.write(str(time.strftime("%d %m %H:%M:%S", time.localtime())) + '\t' + text + '\n')
  log.close()
  #print(str(time.strftime("%d %m %H:%M:%S", time.localtime())) + '\t' + text)


def del_empty_dirs_and_old_files(path):
  data = []
  now = time.time()
  if os.path.isdir(path):
    if len(os.listdir(path)) > 0:
      for x in os.listdir(path):
        if os.path.isdir(os.path.join(path,x)):
          if len(os.listdir(os.path.join(path,x))) == 0:
            os.rmdir(os.path.join(path,x))
          else:
            for y in os.listdir(os.path.join(path,x)):
              if len(os.listdir(os.path.join(path,x,y))) == 0:
                os.rmdir(os.path.join(path,x,y))
              else:
                for z in os.listdir(os.path.join(path,x,y)):
                  if os.path.isfile(os.path.join(path,x,y,z)):
                    if os.stat(os.path.join(path,x,y,z)).st_mtime < now - int(x) * 86400:
                      data.append(os.path.join(path,x,y,z))
                  if os.path.isdir(os.path.join(path,x,y,z)):
                    if len(os.listdir(os.path.join(path,x,y,z))) == 0:
                      os.rmdir(os.path.join(path,x,y,z))
                    else:
                      for a in os.listdir(os.path.join(path,x,y,z)):
                        if os.path.isdir(os.path.join(path,x,y,z,a)):
                          if len(os.listdir(os.path.join(path,x,y,z,a))) == 0:
                            os.rmdir(os.path.join(path,x,y,z,a))
                          else:
                            for b in os.listdir(os.path.join(path,x,y,z,a)):
                              if os.stat(os.path.join(path,x,y,z,a,b)).st_mtime < now - int(x) * 86400:
                                if os.path.isfile(os.path.join(path,x,y,z,a,b)):
                                  data.append(os.path.join(path,x,y,z,a,b))
                    

  return data


def update_video_status(config_sql_server, delete_file, date):
  status = 0
  try:
    connection = pymysql.connect(
        host=config_sql_server[0],
        user=config_sql_server[1],
        password=config_sql_server[2],
        db=config_sql_server[3],
        charset=config_sql_server[4],
        cursorclass=DictCursor
    )
    mycursor = connection.cursor()
    query = """
            UPDATE VIDEO
            SET DELETE_DATE = %s
            WHERE VIDEO.FILE_NAME LIKE %s
            """
    mycursor.execute(query, ( date, delete_file ))
    connection.commit()
    status = mycursor.rowcount
    connection.close()
  except:
    wrait_log('ERROR | file = ' + delete_file + ' and date = ' + date)

  return status

def main():
  del_files = del_empty_dirs_and_old_files(path)
  now = datetime.datetime.now()

  if del_files:
    for t in del_files:
      if len(os.path.basename(t)) < 15:
        os.remove(t)
      if update_video_status(config_sql_server, os.path.basename(t), now.strftime("%Y-%m-%d")):
        os.remove(t)
      else:
        wrait_log('ERROR | file = ' + t + ' and date = ' + now.strftime("%Y-%m-%d"))
    wrait_log('INFO | complited attempt to delete files is over')
  else:
    wrait_log('INFO | complited no files to delete')

while True:
  main()
  time.sleep(5*60*60)
