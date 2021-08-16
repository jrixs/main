#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import urllib
from pymysql.cursors import DictCursor

def get_video_storage(config_sql_server, find_sessionid=None):
    data = []
    connection = pymysql.connect(
        host=config_sql_server[0],
        user=config_sql_server[1],
        password=config_sql_server[2],
        db=config_sql_server[3],
        charset=config_sql_server[4],
        cursorclass=DictCursor
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
            try:
                urllib.request.urlopen('http://'+row['PUBLIC_ADDRESS']+':'+row['PUBLIC_PORT']+'/'+row['STORAGE_DAYS']+'/'+row['RECORDING_DATE'].replace('-','/')+'/'+row['FILE_NAME'])
                data.append({'url': 'http://' + row['PUBLIC_ADDRESS'] + ':' + row['PUBLIC_PORT'] + '/' + row[
                    'STORAGE_DAYS'] + '/' + row['RECORDING_DATE'].replace('-', '/') + '/' + row['FILE_NAME'],
                             'file_name': row['FILE_NAME'],
                             'recording_date': row['RECORDING_DATE'],
                             'storage_days': row['STORAGE_DAYS'],
                             'delete_date': row['DELETE_DATE']
                             })
            except:
                data.append({'url': 'http://' + row['PUBLIC_ADDRESS'] + ':' + row['PUBLIC_PORT'] + '/' + row['STORAGE_DAYS'] + '/' + row['RECORDING_DATE'].replace('-', '_') + '/' + row['FILE_NAME'],
                             'file_name': row['FILE_NAME'],
                             'recording_date': row['RECORDING_DATE'],
                             'storage_days': row['STORAGE_DAYS'],
                             'delete_date': row['DELETE_DATE']
                             })

    connection.close()

    return data

