#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(sys.path[0] + '/lib')
import time
import pymysql
from pymysql.cursors import DictCursor


class opvideo():

    def __init__(self, config=None ):
        self.config = config
        self.log = config[5]  + '/videos_error.log'

    def wrait_log_err(self, text=None):
        self.text = text
        log = open(self.log, 'a')
        log.write(str(time.strftime("%d %m %H:%M:%S", time.localtime())) + '\t' + self.text + '\n')
        log.close()

    def connect(self):
        try:
            connection = pymysql.connect(
                host=self.config[0],
                user=self.config[1],
                password=self.config[2],
                db=self.config[3],
                charset=self.config[4],
                cursorclass=DictCursor
            )
            cursor = connection.cursor()
            return cursor
        except:
            self.wrait_log_err("CONECT ERROR | database does not connect")
            time.sleep(600)
            self.connect()
   

    def get_data_storage(self, zone=None):
        self.zone = zone 
        connect = self.connect()
        if connect != 1:
            sql = "SELECT id,SERVER,USER,RSA_KEY,SPEED,PATH_SRC,PATH_DST,TYPE_VIDEOFILE FROM CONFIG WHERE ZONE LIKE (%s)"
            connect.execute(sql, (self.zone))
            sql_answer = connect.fetchone()
            connect.close()
            if sql_answer == None:
                return None
            else:
                data = [sql_answer['id'],
                        sql_answer['SERVER'],
                        sql_answer['USER'],
                        sql_answer['RSA_KEY'],
                        sql_answer['SPEED'],
                        sql_answer['PATH_SRC'],
                        sql_answer['PATH_DST'],
                        sql_answer['TYPE_VIDEOFILE']]
                return data
        else:
            get_data_storage(self.zone)


    def wrait_data_video(self, data=None):
        self.data = data
        connect = self.connect()
        if connect != 1:
            try:
                sql = "INSERT INTO VIDEO SET ZONE_ID = %s, PROJECTID = %s, SESSIONID = %s, FILE_NAME = %s, RECORDING_DATE = %s, STORAGE_DAYS = %s;"
                connect.execute(sql, (self.data[0], self.data[1], self.data[2], self.data[3], self.data[4], self.data[5]))
                connect.connection.commit()
                connect.close()
            except:
                return 1
        else:
            wrait_data_video(self.data)

