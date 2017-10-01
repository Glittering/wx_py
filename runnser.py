# coding: utf-8
import chardet
import sys

from middle import UnifiedOrderPay

if __name__ == "__main__":
    pay = UnifiedOrderPay('xxxxxxxxx', 'xxxxxx', 'xxxxxxxxxx')
    res = pay.post(body="111".encode('utf-8', 'ignore'), out_trade_no="xxxxxxxxxx", total_fee="1", spbill_create_ip='xxxxxxxx',
                   notify_url='xxxxxxxxxxxxxxx', trade_type='MWEB')
    print(res)
    # print(eval(res)['return_msg'].encode('utf-8'))
    # print(chardet.detect(res['return_msg']))
    print(res['return_msg'].encode('utf-8'))
