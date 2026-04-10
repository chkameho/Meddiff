import requests

BIN_API_URL = r'https://api.jsonbin.io/v3/b'

def load_key(api_key, bin_id, key, empty_value=[]):
    """
    Load key from bin
    """
    url = BIN_API_URL + '/' + bin_id + '/latest'
    headers = {'X-Master-Key': api_key}
    res = requests.get(url, headers=headers).json()
    res = res['record']
    if key in res:
        return res[key]
    else:
        return empty_value


def save_key(api_key, bin_id, key, data):
    """
    Save key to bin
    """
    url = BIN_API_URL + '/' + bin_id
    headers = {'X-Master-Key': api_key, 'Content-Type': 'application/json'}
    res = requests.get(url, headers=headers).json()
    res = res['record']
    if type(res) != dict:
        res = {key:data}  # generate new dict
    else:
        res[key] = data
    res = requests.put(url, headers=headers, json=res).json()
    return res

        
def del_first_count(api_key , bin_id ,username):
    # Laden der Daten
    data = load_key(api_key, bin_id, username)

    # Löschen der Daten
    data = None
    return save_key(api_key, bin_id, username, data)


def load_data(api_key_1, bin_id_1,username):
    load = load_key(api_key_1, bin_id_1, username)
    #Falls keine Daten gespeichert wurde, wird die Daten als eine leere Liste definiert.
    if load == None:
        load=[]
    return load
