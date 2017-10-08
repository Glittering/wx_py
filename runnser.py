# coding: utf-8
import chardet
import sys

from middle import UnifiedOrderPay, JsAPIOrderPay


appid = 'wx0465c5610cb6fdca'
mch_id = '1481242412'
api_key = '192006250b4c09247ec02edce69f6a2e'
app_secret = '319b18bf197078aa5f59f5dd68ec3aba'


def method_redirect_url():
    pass


# if __name__ == "__main__":
#     pay = UnifiedOrderPay('wx0465c5610cb6fdca', '1481242412', '192006250b4c09247ec02edce69f6a2e')
#     res = pay.post(body="111".encode('utf-8', 'ignore'), out_trade_no="123123123123", total_fee="1", spbill_create_ip='120.0.170.77',
#                    notify_url='api.zgtxcj.com', trade_type='MWEB')
#     print(res)
#     # print(eval(res)['return_msg'].encode('utf-8'))
#     # print(chardet.detect(res['return_msg']))
#     print(res['return_msg'].encode('utf-8'))

if __name__ == "__main__":
    pay = JsAPIOrderPay(appid, mch_id, api_key, app_secret)

    # get_code
    code = pay.create_oauth_url_for_code(redirect_uri='')
    print(code)

    print(pay.post_(body='111'.encode('utf-8', 'ignore'), out_trade_no='123123123123', total_fee='1', spbill_create_ip='120.0.170.77',
                   notify_url='api.zgtxcj.com', code=code))
