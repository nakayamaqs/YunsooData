__author__ = 'Zhe'

import requests
import json
import io
from pprint import pprint
from yunsoo.__init__ import __data_server__
from yunsoo.cookies import get_cookie
import codecs

current_cookies = get_cookie()


def data_import(json_file):
    with io.open(json_file, 'r', encoding='utf-8-sig') as data_file:
        data = json.load(data_file)
    # pprint(data)

    payload = data
    result = requests.post(__data_server__ + '/data/import', data=json.dumps(payload),
                           cookies=current_cookies).json()
    return result


def get_work_sheet_input(json_file):
    with io.open(json_file, 'r', encoding='utf-8-sig') as data_file:
        data = json.load(data_file)
    return data


# pprint(get_work_sheet_input('work_sheet_input.json'))
