
import db, os

def get_trigger(check, config_db=None):
    trigger_setings_page = {}

    if check == 'setings_db':
        if not os.path.isfile('db.conf'):
            trigger_setings_page['setingsConnect']  = 'disabled'
            trigger_setings_page['setingsDatabase'] = 'active'
            trigger_setings_page['setingsLDAP']     = 'disabled'
            trigger_setings_page['vpillsConnect']   = ''
            trigger_setings_page['vpillsDatabase']  = 'show active'
            trigger_setings_page['vpillsLDAP']      = ''
            trigger_setings_page['serverdb']        = 'Enter the server name or address'
            trigger_setings_page['schemadb']        = 'Database name'
            trigger_setings_page['userdb']          = 'User name'
            trigger_setings_page['passworddb']      = 'password'
            trigger_setings_page['serverdb_atr']    = ''
            trigger_setings_page['schemadb_atr']    = ''
            trigger_setings_page['userdb_atr']      = ''
            trigger_setings_page['passworddb_atr']  = ''
            trigger_setings_page['schemadb_val']    = ''
            trigger_setings_page['userdb_val']      = ''
            trigger_setings_page['passworddb_val']  = ''
            trigger_setings_page['status_db_init']  = 'badge-danger'
            trigger_setings_page['status_db']       = 'no connected'
            trigger_setings_page['button_db']       = 'Connect'
        else:
            trigger_setings_page['serverdb']        = config_db['server']
            trigger_setings_page['schemadb']        = config_db['schema']
            trigger_setings_page['userdb']          = config_db['user']
            trigger_setings_page['passworddb']      = '*****'
            trigger_setings_page['serverdb_atr']    = 'disabled'
            trigger_setings_page['schemadb_atr']    = 'disabled'
            trigger_setings_page['userdb_atr']      = 'disabled'
            trigger_setings_page['passworddb_atr']  = 'disabled'
            trigger_setings_page['serverdb_val']    = ''
            trigger_setings_page['schemadb_val']    = ''
            trigger_setings_page['userdb_val']      = ''
            trigger_setings_page['passworddb_val']  = ''
            if db.connect({'serverdb': config_db['server'],
                           'schemadb': config_db['schema'],
                           'userdb': config_db['user'],
                           'passworddb': config_db['password']}):
                trigger_setings_page['status_db_init'] = 'badge-success'
                trigger_setings_page['status_db']      = 'connected'
                trigger_setings_page['setingsConnect'] = 'active'
                trigger_setings_page['setingsDatabase'] = ''
                trigger_setings_page['setingsLDAP'] = ''
                trigger_setings_page['vpillsConnect'] = 'show active'
                trigger_setings_page['vpillsDatabase'] = ''
                trigger_setings_page['vpillsLDAP'] = ''
            else:
                trigger_setings_page['status_db_init']  = 'badge-danger'
                trigger_setings_page['status_db']       = 'no connected'
                trigger_setings_page['setingsConnect'] = 'disabled'
                trigger_setings_page['setingsDatabase'] = 'active'
                trigger_setings_page['setingsLDAP'] = 'disabled'
                trigger_setings_page['vpillsConnect'] = ''
                trigger_setings_page['vpillsDatabase'] = 'show active'
                trigger_setings_page['vpillsLDAP'] = ''
            trigger_setings_page['button_db']       = 'Chang'

    if check == 'setings_db':
        if config_db == None:
            trigger_setings_page['f'] = ''
            trigger_setings_page['ffff'] = ''
            trigger_setings_page['fff'] = ''
            trigger_setings_page['ff'] = ''

    return trigger_setings_page