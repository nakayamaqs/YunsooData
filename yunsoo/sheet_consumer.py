__author__ = 'Zhe'

import requests
import json
from yunsoo.cookies import get_cookie
from yunsoo.__init__ import __data_server__
from yunsoo.s3_helper import save_content
current_cookies = get_cookie()


def distinct_list(seq):
    # order preserving
    checked = []
    for e in seq:
        if e not in checked:
            checked.append(e)
    return checked


def get_data_from_1d_sheet(sheet_id, unit_id, val, s3_key):
    # set_current_sheet(id)
    payload = {'sheet_id': sheet_id, 'id': unit_id, 'filter': {'op': 'in', 'val': [val]}}
    result = requests.post(__data_server__ + '/sheet/unit/modify?exec_now=true', data=json.dumps(payload),
                          cookies=current_cookies).json()
    # print(result)

    # set dimensions
    dimension_names = []
    dimension_values = []
    for i, e in enumerate(result['data']['sheet_data']['row']):
        dimension_names.append(e['name'])
        dimension_values = distinct_list(e['data'][1])

    # print(dimension_names)
    # print(dimension_values)

    # generate data array in 2d, with init value as -1.
    raw_data_array = [None for t in range(len(dimension_values))]
    # print(raw_data_array)

    rows = result['data']['sheet_data']['row']
    for i in range(result['data']['sheet_data']['row_size']):
        # for each raw data, get the index of product_list
        index_of_1st_dm = dimension_values.index(rows[0]['data'][1][i])
        raw_data_array[index_of_1st_dm] = result['data']['sheet_data']['meas_data'][0][i]

    # convert to dictionary and then json result
    final_result = {
        "dimensions": {
            "values": dimension_values,
            "names": dimension_names
        },
        "data": raw_data_array
    }
    print(json.dumps(final_result, ensure_ascii=False))
    save_content(s3_key, json.dumps(final_result, ensure_ascii=False))

# URL to query:  http://54.223.135.72:8001/sheet?id=4.S.19740602643438
def get_data_from_2d_sheet(sheet_id, unit_id, val, s3_key):
    # set_current_sheet(id)
    # result = requests.get(__data_server__ + '/sheet?id=%s' % id, cookies=current_cookies).json()
    payload = {'sheet_id': sheet_id, 'id': unit_id, 'filter': {'op': 'in', 'val': [val]}}
    result = requests.post(__data_server__ + '/sheet/unit/modify?exec_now=true', data=json.dumps(payload),
                          cookies=current_cookies).json()  # print(result)

    #  set dimensions
    dimension_names = []
    dimension_values = [[], []]
    for i, e in enumerate(result['data']['sheet_data']['row']):
        dimension_names.append(e['name'])
        dimension_values[i] = distinct_list(e['data'][1])

    # generate data array in 2d, with init value as -1.
    raw_data_array = [[None for t in range(len(dimension_values[1]))] for x in range(len(dimension_values[0]))]
    # print(raw_data_array)

    rows = result['data']['sheet_data']['row']
    for i in range(result['data']['sheet_data']['row_size']):
        index_of_product = dimension_values[0].index(
            rows[0]['data'][1][i])  # for each raw data, get the index of product_list
        index_of_date = dimension_values[1].index(
            rows[1]['data'][1][i])  # for each raw data, get the index of date_list
        raw_data_array[index_of_product][index_of_date] = result['data']['sheet_data']['meas_data'][0][i]


    # convert to dictionary and then json result
    final_result = {
        "dimensions": {
            "values": dimension_values,
            "names": dimension_names
        },
        "data": raw_data_array
    }
    print(json.dumps(final_result, ensure_ascii=False))
    save_content(s3_key, json.dumps(final_result, ensure_ascii=False))

def set_current_sheet(id):
    headers = {'Content-Type': 'application/json'}
    payload = {'id': id}
    response = requests.post(__data_server__ + '/sheet/current', headers=headers, data=json.dumps(payload),
                             cookies=current_cookies)
    # print('status-code: ' + str(response.status_code))
    # print(' set current sheet: ' + str(response.json()))

def get_val_by_key(id, key):
    headers = {'Content-Type': 'application/json'}
    payload = {'id': id, 'key': key, 'prop': 'ele_content'}
    response = requests.get(__data_server__ + '/sheet/unit', headers=headers, params=payload, cookies=current_cookies)
    # print(' get_val_by_key: ' + str(response.json()))
    return response.json()['data']['ele_content']['ele_list']['data'][0][0]
