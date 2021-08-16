#!/usr/bin/python3                                                                                                                                                                                                               
# -*- coding: utf-8 -*-                                                                                                                                                                                                          
import ldap                                                                                                                                                                                                                      
from flask import request,render_template     
from flask import Flask, session, redirect
from hashlib import sha1
import datetime 
import db

app = Flask(__name__)
app.secret_key = 'any random string'         
active_users={}

BASE_URL = "http://domain.ru"
access_grp=''
                                                                                                                                                                                                                                 
# LDAP params                                                                                                                                                                                                                    
DC_SERVER = ''
ldap_bind_user=''
ldap_bind_pwd=''
basedn = ""

# MySQL params
config_sql_server = ['domain.ru',                   #'server'
                     '',                            #'user'
                     '',                            #'password'
                     '',                            #'schema'
                     'utf8'                         #'encoding'
                     ]

def get_ldap():
    ldap.set_option(ldap.OPT_REFERRALS, 0)
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    l = ldap.initialize('ldaps://%s:636' % DC_SERVER, trace_level=0)
    l.simple_bind(ldap_bind_user, ldap_bind_pwd)
    l.result()
    return l

def check_grp(login):
    l = get_ldap()
    rsp = l.search_s(basedn, ldap.SCOPE_SUBTREE, 'sAMAccountName=%s'%login, ['memberOf'])
    for i in rsp[0][1]['memberOf']:
        if i.decode('utf8') == access_grp:
            return True
    return False

def check_auth(username,password):
    if '@' not in username:
        username=username+'@domain.ru'
    l=ldap.initialize('ldap://%s:389' %DC_SERVER)
    l.protocol_version = ldap.VERSION3
    if password:
        try:
            l.simple_bind(username, password)
            l.result()
            return check_grp(username.split('@')[0])
        except:
            return False
    return False

@app.route('/login', methods=['POST','GET'])
def login_page():
    if request.method != "POST":
        return render_template('login.html')

    if not request.form['login']:
        return render_template('login.html', error='Укажите логин')
        
    if not request.form['password']:
        return render_template('login.html', error='Укажите пароль')

    if not check_auth(request.form['login'],request.form['password']):
        return render_template("login.html", error='Неверный пароль')

    m = sha1()
    m.update(str(datetime.datetime.now()).encode('utf8'))
    user_hash = m.hexdigest()
    session['hash']=user_hash
    active_users[user_hash]={'login': request.form['login'],
                             'password': request.form['password']
                             }
    return redirect(BASE_URL+'/opvideo', code=302)


@app.route('/', methods=['POST','GET'])
@app.route('/opvideo', methods=['POST','GET'])
def find_video():
    if not 'hash' in session:
        return redirect(BASE_URL+'/login', code=302)

    if session['hash'] not in active_users:
        return redirect(BASE_URL+'/login', code=302)

    if request.method == "POST":

        if not request.form['naus']:
            return render_template('opvideo.html', error='Укажите значения для поиска')

        if len(request.form['naus']) < 5:
            return render_template('opvideo.html', error='Ввели неправильно значение для поиска')

        return render_template('opvideo.html', videos=db.get_video_storage(config_sql_server, request.form['naus']))

    return render_template('opvideo.html')


app.debug = True
app.config['UPLOAD_FOLDER'] = '/tmp'
app.run(host='0.0.0.0', port=8080, threaded=True)
