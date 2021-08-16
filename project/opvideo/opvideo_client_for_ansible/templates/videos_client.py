#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append(sys.path[0] + '/lib')
import socket
import videos_db
import time
import configparser
import os
import re
import glob
import subprocess
from distutils.version import LooseVersion

def connect_db():
    parser = configparser.RawConfigParser()
    file = '/opt/custom/opvideo/db.conf'
    parser.read(file)
    config_tmp = dict(parser.items('videos-config'))
    config = [config_tmp['server'],
              config_tmp['user'],
              config_tmp['password'],
              config_tmp['schema'],
              config_tmp['encoding'],
              config_tmp['path_log']]
    return config

config = connect_db()
hostname = socket.gethostbyaddr(socket.gethostbyname('docker1'))[0]
zone = hostname[hostname.find(".")+1:].split(".")[0]
DB = videos_db.opvideo(config)
config_video_storage = DB.get_data_storage(zone)
ver_NSP = str(re.search(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', subprocess.check_output('nausoftphone --version', shell=True).decode('utf-8')).group(0))

if ver_NSP is None:
    raise SystemExit(1)

def patch_1(ver, step1 = None):
    if LooseVersion(ver) < LooseVersion('7.4.53.5'): # В версии NP 7.4.53.5 изменился формат записи date в профиле NSP
        if step1 is None:
            return glob.glob(config_video_storage[5] + '*/*/*.' + config_video_storage[7])
        if step1 is not None:
            return str(re.search(r'\d{4}_\d{1,2}_\d{1,2}', step1).group(0))
    else:
        if step1 is None:
            return glob.glob(config_video_storage[5] + '*/*/*/*/*.' + config_video_storage[7])
        if step1 is not None:
            return str(re.search(r'\d{4}/\d{1,2}/\d{1,2}', step1).group(0))

def start_sync():
    files = []
    files_tmp = patch_1(ver_NSP)

    for mfile in files_tmp:
        try:
            subprocess.check_output(["fuser", "-u", mfile])
        except:
            if len(os.path.basename(mfile))>15:
                files.append(mfile)
            else:
                os.remove(mfile)            

    if files:

        key_rsa = open('/opt/custom/opvideo/key_rsa', 'w')
        key_rsa.write(config_video_storage[3])
        key_rsa.close()
        os.system("chmod 600 /opt/custom/opvideo/key_rsa")

        cmd = "rsync -e \"ssh -o StrictHostKeyChecking=no -i /opt/custom/opvideo/key_rsa\" -vaz --bwlimit=" + config_video_storage[4] + " --min-size=1 \"" + config_video_storage[5] + "\" " + config_video_storage[2] + "@" + config_video_storage[1] + ":\"" + config_video_storage[6] + "\" > /dev/null 2>>" + config[5] + "/op_rsync.log"

        if subprocess.call(cmd, shell=True) == 0:

            for exampl in files:
                data = []
                try:
                    daterecord = patch_1(ver_NSP, exampl)
                    mdays2 = re.search(r'/\d{1,2}/', exampl)
                    mdays1 = str(mdays2.group(0))
                    mdays = mdays1[mdays1.find("/")+1:].split("/")[0]
                    name = os.path.basename(exampl)
                    mtime2 = re.search(r'\d{2}-\d{2}-\d{2}-', name)
                    mtime1 = str(mtime2.group(0))
                    mid1 = name.replace(mtime1, '')
                    projectid = mid1.split("-")[0]
                    mid2 = mid1.replace(projectid+'-', '')
                    sessionid = mid2.split(".")[0]
                    data = [ str(config_video_storage[0]), projectid, sessionid, name, daterecord, mdays]
                except:
                    DB.wrait_log_err("FORMAT ERROR | file name format is not correct: " + exampl)
                    continue

                if sessionid != '':
                    if DB.wrait_data_video(data):
                        DB.wrait_log_err("SQL ERROR | wrait_data_video values: " + str(config_video_storage[0]) + " " + projectid + " " + sessionid + " " + name + " " + daterecord + " " + mdays)
                    else:
                        cmd_rm = "rm " + exampl + " >> " + config[5] + "/op_rsync.log"
                        if subprocess.call(cmd_rm, shell=True) != 0: 
                            DB.wrait_log_err("REMOVE ERROR | not delete: " + exampl)
                else:
                    cmd_rm = "rm " + exampl + " >> " + config[5] + "/op_rsync.log"
                    if subprocess.call(cmd_rm, shell=True) != 0:
                        DB.wrait_log_err("REMOVE ERROR | not delete: " + exampl)

        else:
            DB.wrait_log_err("RSYNC ERROR | CMD: " + cmd)

def del_empty_dirs(path, P = True):
    if os.path.isdir(path):
        if len(os.listdir(path)) > 0:
            for x in os.listdir(path):
                if os.path.isdir(os.path.join(path,x)):
                    if len(os.listdir(os.path.join(path,x))) == 0: os.rmdir(os.path.join(path,x))
                    else: del_empty_dirs(os.path.join(path,x))
            if P: del_empty_dirs(path, False)
        else: os.rmdir(path)

while True:
    start_sync()
    del_empty_dirs(config_video_storage[5])
    time.sleep(3600)
