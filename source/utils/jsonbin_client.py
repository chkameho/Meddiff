import requests

BIN_API_URL = r'https://api.jsonbin.io/v3/b'

def load_key(api_key, bin_id, key, empty_value=[]):
    """
    Retrieve a specific key from a JSONBin record.

    Args:
        api_key (str): JSONBin master key for authentication.
        bin_id (str): ID of the JSONBin bin.
        key (str): Key to retrieve from the stored JSON object.
        default (Any, optional): Value returned if key does not exist.

    Returns:
        Any: Value stored under `key`, or `default` if not found.
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
    Save or update a key in a JSONBin record.

    This function:
    - Loads the existing bin content
    - Updates a single key
    - Writes the full updated object back

    Args:
        api_key (str): JSONBin master key.
        bin_id (str): ID of the JSONBin bin.
        key (str): Key to update.
        data (Any): Value to store.

    Returns:
        dict: Response from JSONBin API.
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

def load_data(api_key, bin_id, username):
    """
    Load user-specific data from JSONBin.

    If the user has no stored data, returns an empty list.

    Args:
        api_key (str): JSONBin master key.
        bin_id (str): ID of the JSONBin bin.
        username (str): Key representing the user.

    Returns:
        list: Stored user data or empty list if none exists.
    """
    
    load =load_key(api_key, bin_id, username)
    if load == None:
        load=[]
    return load
