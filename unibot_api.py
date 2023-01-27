import requests

api = 'https://api.unipjsk.com/api'


def alias_to_songid(alias):
    response = requests.get(url=f'{api}/getsongid/{alias}')
    response_json = response.json()

    response.close()

    if response_json['status'] == 'false':
        return 0
    else:
        return response_json['musicId']