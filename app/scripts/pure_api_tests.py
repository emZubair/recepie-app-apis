import requests


BASE_URL = 'http://127.0.0.1:8000/'
ENDPOINT = 'api/updates/'


def get_list():
    response = requests.get(BASE_URL + ENDPOINT)
    data = response.json()
    print(type(data))
    for value in data:
        details = requests.get(BASE_URL+ENDPOINT+str(value.get('id')))
        print(details.json())
        # print(value.get('id'))

    return data


# print(get_list())
get_list()
