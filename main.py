"""
  This is the Entry of this python data service consumer.
"""
__author__ = 'Zhe'

from yunsoo.sheet_consumer import *
import datetime

class Hello:
    def __init__(self):
        pass

    def sayHello(self):
        print("This is Hello! -> by " + self)

# work_sheet_id = ['4.S.19739162398753', '4.S.19740602643438', '4.S.19738931498116','4.S.19739337276415']
# company_unit_id = ['4.SA.组织ID.19739176367353','4.SA.组织ID.19740604775335','4.SA.组织ID.19738938410218','4.SA.组织ID.19739861318573']
org_id = ['2k0r0963j0akld83lsd2', '2k0r1l55i2rs5544wz5', '2k0r2yvydbxbvibvgfm', '2k0r306o609oljxd1hh',
          '2kbyyjauwtate9syvmy']

work_sheet_input = {
    '4.S.19739162398753': {
        'company_unit_id': '4.SA.组织ID.19739176367353',
        'dimension': '2D',
        'name': 'product_month_scan_count'
    },
    '4.S.19740602643438': {
        'company_unit_id': '4.SA.组织ID.19740604775335',
        'dimension': '1D',
        'name': 'product_qrcode_count'
    },
    '4.S.19738931498116': {
        'company_unit_id': '4.SA.组织ID.19738938410218',
        'dimension': '1D',
        'name': 'product_scan_count'
    },
    '4.S.19739337276415': {
        'company_unit_id': '4.SA.组织ID.19739861318573',
        'dimension': '1D',
        'name': 'location_scan_count'
    }
}

for i, e in enumerate(work_sheet_input):
    # print(i,e)
    set_current_sheet(e)
    val = get_val_by_key(work_sheet_input[e]['company_unit_id'], '2k0r1l55i2rs5544wz5')
    the_key_tail = str(datetime.datetime.now().year) + str('%02d' % datetime.datetime.now().month) + str(datetime.datetime.now().day)
    s3_key = '/report/organization/2k0r1l55i2rs5544wz5/' + work_sheet_input[e]['name'] + '/' + the_key_tail
    if work_sheet_input[e]['dimension'] == '2D':
        get_data_from_2d_sheet(e, work_sheet_input[e]['company_unit_id'], val, s3_key)
    else:
        get_data_from_1d_sheet(e, work_sheet_input[e]['company_unit_id'], val, s3_key)

    print('Finish retrieve data for item ' + str(i + 1) + '\n')

# Hello.sayHello(__author__)
# print(get_data_from_2d_sheet('4.S.19739162398753'))  # 产品扫码月统计
# print(get_data_from_1d_sheet('4.S.19740602643438'))  # 产品贴码统计
# print(get_data_from_1d_sheet('4.S.19738931498116'))  # 产品扫码统计
# print(get_data_from_1d_sheet('4.S.19739337276415'))  # 产品扫码地域统计
