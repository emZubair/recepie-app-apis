from json import dumps
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


def create_update():
    data = {
        "user": 1,
        "content": "Lonng time, new post"
    }

    response = requests.post(BASE_URL + ENDPOINT, data=dumps(data))
    print(response.status_code)
    print(response.headers)
    print(response.json())


def create_put():
    data = {
        'id': 5,
        'content': "Updated by PUTTT"
    }

    response = requests.put(BASE_URL + ENDPOINT + "1/", data=dumps(data))
    print(response.status_code)
    print(response.headers)
    print(response.json())


def create_delete():
    response = requests.delete(BASE_URL + ENDPOINT + "7/")
    print(response.status_code)
    print(response.headers)
    print(response.json())


# print(get_list())
# create_delete()
# get_list()

# create_update()
create_put()
