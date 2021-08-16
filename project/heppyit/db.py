#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import pymysql
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
#from pymysql.cursors import DictCursor

'''def get_video_storage(config_sql_server, find_sessionid=None):
    data = []
    connection = pymysql.connect(
        host=config_sql_server[0],
        user=config_sql_server[1],
        password=config_sql_server[2],
        db=config_sql_server[3],
        charset=config_sql_server[4],
        cursorclass=DictCursor3
    )
    
    with connection.cursor() as cursor:
        query = """
                SELECT
                   PUBLIC_ADDRESS,PUBLIC_PORT,STORAGE_DAYS,CAST(RECORDING_DATE AS CHAR) 'RECORDING_DATE',FILE_NAME,CAST(DELETE_DATE AS CHAR) 'DELETE_DATE'
                FROM
                   VIDEO
                INNER JOIN CONFIG ON CONFIG.id=VIDEO.ZONE_ID
                WHERE SESSIONID LIKE (%s)
                """
        cursor.execute(query, (find_sessionid))
        for row in cursor:
            data.append({'url': 'http://'+row['PUBLIC_ADDRESS']+':'+row['PUBLIC_PORT']+'/'+row['STORAGE_DAYS']+'/'+row['RECORDING_DATE'].replace('-','_')+'/'+row['FILE_NAME'],
                         'file_name': row['FILE_NAME'],
                         'recording_date': row['RECORDING_DATE'],
                         'storage_days': row['STORAGE_DAYS'],
                         'delete_date': row['DELETE_DATE']
                         })

    connection.close()

    return data
'''
def connect(data):
    connection = None
    try:
        connection = psycopg2.connect(user     = data['userdb'],
                                      password = data['passworddb'],
                                      host     = data['serverdb'],
                                      port     = "5432",
                                      database = data["schemadb"])
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        return 0

def get_group(data):
    try:
        postgreSQL_select_Query = "select id,name from heppyit.group_pc gp where owner is null"
        tdata = []
        connection = psycopg2.connect(user=data['user'],
                                      password=data['password'],
                                      host=data['server'],
                                      port="5432",
                                      database=data["schema"])
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            tdata.append({'id': row['id'],
                          'name': row['name'],
                          'owner': get_group_other(cursor,
                                                   "select id,name from heppyit.group_pc gp where owner = " + str(
                                                       row['id']))})
        cursor.close()
        connection.close()
        return tdata
    except (Exception, Error) as error:
        return 0

def get_group_other(cursor,sql):
    try:
        data = []
        cursor.execute(sql)
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            data.append({'id': row['id'],
                          'name': row['name']})
        return data
    except(Exception, Error) as error:
        return 0

