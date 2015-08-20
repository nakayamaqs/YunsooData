#!/usr/bin/python
#coding:utf-8
"""
  This is the Entry of this python data service consumer.
"""

__author__ = 'Zhe'

from yunsoo.sheet_consumer import *
from yunsoo.data_import import *
# import datetime
from datetime import date, timedelta
import calendar
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')
os_path = os.path.abspath(os.path.dirname(sys.argv[0]))

def get_current_path():
    if os.name == 'nt':
        return ''
    else:
        return os.path.abspath(os.path.dirname(sys.argv[0]))+'/'

def run_report(org_list, work_sheet_list, the_key_tail, from_day, end_day):
    if data_import(get_current_path() + 'yunsoo/datamodel.json')['status'] == 'ok':
        for o in org_list:
            print("Working on org: " + str(o))
            for i, e in enumerate(work_sheet_list):
                set_current_sheet(e)
                val = get_val_by_key(work_sheet_list[e]['company_unit_id'], str(o))
                from_date_key = str(from_day.year) + str('%02d' % from_day.month) + str('%02d' % from_day.day)
                end_date_key = str(end_day.year) + str('%02d' % end_day.month) + str('%02d' % end_day.day)
                s3_key = '/report/organization/' + str(o) + '/' + work_sheet_list[e]['name'] + '/' + the_key_tail

                if work_sheet_list[e]['dimension'] == '2D':
                    get_data_from_2d_sheet(e, work_sheet_list[e]['company_unit_id'], val,
                                           work_sheet_list[e]['datetime_unit_id'],
                                           [from_date_key, end_date_key],
                                           s3_key)
                else:
                    # get_data_from_1d_sheet(e, work_sheet_input[e]['company_unit_id'], val, s3_key)
                    get_data_from_1d_sheet(e, work_sheet_list[e]['company_unit_id'], val,
                                           work_sheet_list[e]['datetime_unit_id'],
                                           [from_date_key, end_date_key],
                                           s3_key)

                print('Finish retrieve data for item ' + str(i + 1) + '\n')
    else:
        print("Failed to update data model! Please contact with the DEV Team.")


        # Hello.sayHello(__author__)
        # print(get_data_from_2d_sheet('4.S.19739162398753'))  # 产品扫码月统计
        # print(get_data_from_1d_sheet('4.S.19740602643438'))  # 产品贴码统计
        # print(get_data_from_1d_sheet('4.S.19738931498116'))  # 产品扫码统计
        # print(get_data_from_1d_sheet('4.S.19739337276415'))  # 产品扫码地域统计


        # work_sheet_input = {
        #     '4.S.19739162398753': {
        #         'company_unit_id': '4.SA.组织ID.19739176367353',
        #         'datetime_unit_id': '4.SA.日期.19739176353953',
        #         'dimension': '2D',
        #         'name': 'product_month_scan_count'
        #     },
        #     '4.S.19740602643438': {
        #         'company_unit_id': '4.SA.组织ID.19740604775335',
        #         'datetime_unit_id': '',
        #         'dimension': '1D',
        #         'name': 'product_qrcode_count'
        #     },
        #     '4.S.19738931498116': {
        #         'company_unit_id': '4.SA.组织ID.19738938410218',
        #         'datetime_unit_id': '4.SA.日期.19738938396608',
        #         'dimension': '1D',
        #         'name': 'product_scan_count'
        #     },
        #     '4.S.19739337276415': {
        #         'company_unit_id': '4.SA.组织ID.19739861318573',
        #         'datetime_unit_id': '4.SA.日期.19739861304002',
        #         'dimension': '1D',
        #         'name': 'location_scan_count'
        #     }
        # }


def get_ful_key_tail(the_date):
    return str(the_date.year) + str('%02d' % the_date.month) + str('%02d' % the_date.day)


def main_run():
    # org_id_list = ['2k0r0963j0akld83lsd2', '2k0r1l55i2rs5544wz5', '2k0r2yvydbxbvibvgfm', '2k0r306o609oljxd1hh',
    #                '2kbyyjauwtate9syvmy', '2khxnw8yfxoga6eubib', '2khxwnl3092c2ygmbik']
    org_id_list = ['2k0r1l55i2rs5544wz5', '2khxwnl3092c2ygmbik', '2khxnw8yfxoga6eubib', '2knt1rqv6pp28dqlr80']

    # org_id_list = ['2k0r1l55i2rs5544wz5']
    work_sheet_input = get_work_sheet_input(get_current_path()+ 'yunsoo/work_sheet_input.json')

    # run yesterday's report
    yesterday_key = date.today() - timedelta(1)  # every day run yesterday's report
    yesterday_key_tail = str(yesterday_key.year) + str('%02d' % yesterday_key.month) + str('%02d' % yesterday_key.day)
    run_report(org_id_list, work_sheet_input, yesterday_key_tail, yesterday_key, yesterday_key)

    # run last week's report
    if yesterday_key.weekday() == 0:
        from_date = yesterday_key - timedelta(7)
        end_date = yesterday_key - timedelta(1)
        file_key_tail = get_ful_key_tail(from_date) + str("-") + get_ful_key_tail(end_date)
        run_report(org_id_list, work_sheet_input, file_key_tail, from_date, end_date)

    # run last month's report
    if yesterday_key.day == 1:
        end_date = yesterday_key - timedelta(1)  # get end day of last month
        w, today_days = calendar.monthrange(end_date.year, end_date.month)
        from_date = yesterday_key - timedelta(today_days)
        file_key_tail = str(from_date.year) + str('%02d' % from_date.month)
        run_report(org_id_list, work_sheet_input, file_key_tail, from_date, end_date)


main_run()
