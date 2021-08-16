#!/usr/bin/python3                                                                                                                                                                                                               
# -*- coding: utf-8 -*-                                                                                                                                                                                                          

from flask import request,render_template     
from flask import Flask, session, redirect
from hashlib import sha1
import datetime, configparser, db, ldap, os, for_html

app = Flask(__name__)
app.secret_key = 'any random string'         
active_users={}
trigger_setings_page = {}

# LDAP params                                                                                                                                                                                                                    
DC_SERVER = ''
ldap_bind_user=''
ldap_bind_pwd=''
basedn = ""
access_grp=''



def load_settings_db(name_conf):
    if os.path.isfile('db.conf'):
        parser = configparser.RawConfigParser()
        file = 'db.conf'
        parser.read(file)
        return dict(parser.items(name_conf))

def save_settings_db(data):
    config = configparser.ConfigParser()
    config['postgresql'] = {'server'  : data['server'],
                            'user'    : data['user'],
                            'password': data['password'],
                            'schema'  : data['schema'],
                            'encoding': 'utf8'}  # encoding
    with open('db.conf', 'w') as configfile:
        config.write(configfile)

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

def check_authoriz():
    if not 'hash' in session:
        return 1
    if session['hash'] not in active_users:
        return 1

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
    return redirect('/home', code=302)

@app.route('/', methods=['POST','GET'])
@app.route('/home', methods=['POST','GET'])
def home():
    if check_authoriz(): return redirect('/login', code=302)
    return render_template('home.html')

@app.route('/connect', methods=['POST','GET'])
def connect():
    if check_authoriz(): return redirect('/login', code=302)
    return render_template('connect.html')

@app.route('/setings', methods=['GET'])
def setings():
    if check_authoriz(): return redirect('/login', code=302)
    return render_template('setings.html', **trigger_setings_page, s_group=db.get_group(load_settings_db('postgresql')))

@app.route('/set_database', methods=['POST'])
def set_database():
    trigger_setings_page = for_html.get_trigger('setings_db', load_settings_db('postgresql'))

    if trigger_setings_page['button_db'] == 'Connect':
        if not request.form['serverdb']:
            trigger_setings_page.update({'serverdb_val': 'is-invalid'})
            return render_template('setings.html', **trigger_setings_page)
        if not request.form['schemadb']:
            trigger_setings_page.update({'schemadb_val': 'is-invalid'})
            trigger_setings_page.update({'serverdb_val': ''})
            trigger_setings_page.update({'serverdb_vol': request.form['serverdb']})
            return render_template('setings.html', **trigger_setings_page)
        if not request.form['userdb']:
            trigger_setings_page.update({'userdb_val': 'is-invalid'})
            trigger_setings_page.update({'serverdb_val': ''})
            trigger_setings_page.update({'serverdb_vol': request.form['serverdb']})
            trigger_setings_page.update({'schemadb_val': ''})
            trigger_setings_page.update({'schemadb_vol': request.form['schemadb']})
            return render_template('setings.html', **trigger_setings_page)
        if not request.form['passworddb']:
            trigger_setings_page.update({'passworddb_val': 'is-invalid'})
            trigger_setings_page.update({'serverdb_val': ''})
            trigger_setings_page.update({'serverdb_vol': request.form['serverdb']})
            trigger_setings_page.update({'schemadb_val': ''})
            trigger_setings_page.update({'schemadb_vol': request.form['schemadb']})
            trigger_setings_page.update({'userdb_val': ''})
            trigger_setings_page.update({'userdb_vol': request.form['userdb']})
            return render_template('setings.html', **trigger_setings_page)
        trigger_setings_page.update({'passworddb_val': ''})
        if db.connect({'serverdb': request.form['serverdb'],
                       'schemadb': request.form['schemadb'],
                       'userdb': request.form['userdb'],
                       'passworddb': request.form['passworddb']}):
            trigger_setings_page.update({'serverdb_val': ''})
            trigger_setings_page.update({'serverdb_vol': request.form['serverdb']})
            trigger_setings_page.update({'schemadb_val': ''})
            trigger_setings_page.update({'schemadb_vol': request.form['schemadb']})
            trigger_setings_page.update({'userdb_val': ''})
            trigger_setings_page.update({'userdb_vol': request.form['userdb']})
            trigger_setings_page.update({'passworddb_val': ''})
            trigger_setings_page.update({'passworddb_vol': '****'})
            trigger_setings_page.update({'status_db_init': 'badge-success'})
            trigger_setings_page.update({'status_db': 'connected'})
            trigger_setings_page.update({'setingsLDAP': ''})
            trigger_setings_page.update({'setingsConnect': ''})
            trigger_setings_page.update({'serverdb_atr': 'disabled'})
            trigger_setings_page.update({'schemadb_atr': 'disabled'})
            trigger_setings_page.update({'userdb_atr': 'disabled'})
            trigger_setings_page.update({'passworddb_atr': 'disabled'})
            trigger_setings_page.update({'button_db': 'Chang'})
        if trigger_setings_page['status_db'] == 'connected':
            save_settings_db({'server': request.form['serverdb'],
                              'schema': request.form['schemadb'],
                              'user': request.form['userdb'],
                              'password': request.form['passworddb']})
        return render_template('setings.html', **trigger_setings_page)
    else:
        trigger_setings_page.update({'vpillsConnect': ''})
        trigger_setings_page.update({'vpillsDatabase': 'show active'})
        trigger_setings_page.update({'vpillsLDAP': ''})
        trigger_setings_page.update({'setingsLDAP': 'disabled'})
        trigger_setings_page.update({'setingsConnect': 'disabled'})
        trigger_setings_page.update({'serverdb_atr': ''})
        trigger_setings_page.update({'schemadb_atr': ''})
        trigger_setings_page.update({'userdb_atr': ''})
        trigger_setings_page.update({'passworddb_atr': ''})
        trigger_setings_page.update({'serverdb_vol': ''})
        trigger_setings_page.update({'schemadb_vol': ''})
        trigger_setings_page.update({'userdb_vol': ''})
        trigger_setings_page.update({'passworddb_vol': ''})
        trigger_setings_page.update({'status_db_init': 'badge-danger'})
        trigger_setings_page.update({'status_db': 'no connected'})
        trigger_setings_page.update({'button_db': 'Connect'})

        return render_template('setings.html', **trigger_setings_page)


@app.route('/set_ldap', methods=['POST'])
def set_ldap():
    trigger_setings_page = for_html.get_trigger('setings_ldap', load_settings_db('ldap'))


#@app.route("/save_db_conf", methods=['POST'])
#def save_db_conf():
#    #Moving forward code
#    forward_message = "Moving Forward..."
#    return render_template('index.html', forward_message=forward_message);

#@app.route('/_get_current_user')
#def get_current_user():
#    return jsonify(username=g.user.username,
#                   email=g.user.email,
#                   id=g.user.id)



@app.route('/test', methods=['POST','GET'])
def test():
    if check_authoriz(): return redirect('/login', code=302)
    return str(datetime.datetime.now())
#return render_template('home.html')

#@app.route('/opvideo', methods=['POST','GET'])
#def find_video():
#    if not 'hash' in session:
#        return redirect('/login', code=302)
#
#    if session['hash'] not in active_users:
#        return redirect('/login', code=302)
#
#    if request.method == "POST":
#
#        if not request.form['naus']:
#            return render_template('opvideo.html', error='Укажите значения для поиска')
#
#        if len(request.form['naus']) < 40:
#            return render_template('opvideo.html', error='Ввели неправильно значение для поиска')
#
#        return render_template('opvideo.html', videos=db.get_video_storage(config_sql_server, request.form['naus']))
#
#    return render_template('opvideo.html')


trigger_setings_page = for_html.get_trigger('setings_db', load_settings_db('postgresql'))
app.debug = True
app.config['UPLOAD_FOLDER'] = '/tmp'
app.run(host='0.0.0.0', port=80, threaded=True)
