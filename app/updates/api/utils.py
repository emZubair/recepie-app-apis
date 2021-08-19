from json import loads


def is_valid_json(json_data):
    is_valid = True
    try:
        _ = loads(json_data)
    except ValueError:
        is_valid = False
    return is_valid
