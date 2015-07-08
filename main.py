"""
  This is the Entry of this python data service consumer.
"""
__author__ = 'Zhe'

from yunsoo.sheet_consumer import *
from yunsoo.data_import import *
# import datetime
from datetime import date, timedelta


def run_report(org_list, work_sheet_list, the_date_key_tail):
    if data_import('yunsoo/datamodel.json')['status'] == 'ok':
        for o in org_id_list:
            print("Working on org: " + str(o))
            for i, e in enumerate(work_sheet_input):
                set_current_sheet(e)
                val = get_val_by_key(work_sheet_input[e]['company_unit_id'], str(o))
                s3_key = '/report/organization/' + str(o) + '/' + work_sheet_input[e]['name'] + '/' + the_date_key_tail

                if work_sheet_input[e]['dimension'] == '2D':
                    get_data_from_2d_sheet(e, work_sheet_input[e]['company_unit_id'], val,
                                           work_sheet_input[e]['datetime_unit_id'],
                                           [the_date_key_tail, the_date_key_tail],
                                           s3_key)
                else:
                    # get_data_from_1d_sheet(e, work_sheet_input[e]['company_unit_id'], val, s3_key)
                    get_data_from_1d_sheet(e, work_sheet_input[e]['company_unit_id'], val,
                                           work_sheet_input[e]['datetime_unit_id'],
                                           [the_date_key_tail, the_date_key_tail],
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


org_id_list = ['2k0r0963j0akld83lsd2', '2k0r1l55i2rs5544wz5', '2k0r2yvydbxbvibvgfm', '2k0r306o609oljxd1hh',
               '2kbyyjauwtate9syvmy']
# org_id_list = ['2kbyyjauwtate9syvmy']

work_sheet_input = get_work_sheet_input('yunsoo/work_sheet_input.json')
the_day = date.today() - timedelta(1)  # every day run yesterday's report
the_key_tail = str(the_day.year) + str('%02d' % the_day.month) + str('%02d' % the_day.day)

run_report(org_id_list, work_sheet_input, the_key_tail)
