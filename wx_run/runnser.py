# coding: utf-8
import urllib.parse

import chardet
import sys

import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .middle import UnifiedOrderPay, JsAPIOrderPay

appid = 'wx0465c5610cb6fdca'
mch_id = '1481242412'
api_key = '192006250b4c09247ec02edce69f6a2e'
app_secret = '319b18bf197078aa5f59f5dd68ec3aba'


@api_view(['GET', 'POST'])
def method_redirect_url():
    pass


@api_view(['GET', 'POST'])
def place_order(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    print(ip)

    pay = UnifiedOrderPay('wx0465c5610cb6fdca', '1481242412', '192006250b4c09247ec02edce69f6a2e')
    res = pay.post(body="111".encode('utf-8', 'ignore'), out_trade_no="23232323", total_fee="1",
                   spbill_create_ip=ip,
                   notify_url='api.zgtxcj.com', trade_type='MWEB')
    print(res)
    # print(eval(res)['return_msg'].encode('utf-8'))
    # print(chardet.detect(res['return_msg']))
    print(res['return_msg'].encode('utf-8'))
    return Response(res['mweb_url'].encode('utf-8'))


# {'return_code': 'SUCCESS', 'return_msg': 'OK', 'trade_type': 'MWEB', 'prepay_id': 'wx201710091320367ceaf4391a0829915306', 'mch_id': '1481242412', 'nonce_str': 'dqhNMjjf2xbPLt9w', 'result_code': 'SUCCESS', 'appid': 'wx0465c5610cb6fdca', 'mweb_url': 'https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?prepay_id=wx201710091320367ceaf4391a0829915306&package=3308721725'}
# b'OK'


@api_view(['GET', 'POST'])
def mid_order(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    print(ip)

    url = 'http://wx.zgtxcj.com' + request.get_full_path()
    # url = request.get_host() + request.get_full_path()

    pay = JsAPIOrderPay(appid, mch_id, api_key, app_secret)

    # get_code
    code = pay.create_oauth_url_for_code(redirect_uri=url)
    res = requests.get(code)
    print(dir(res))
    print(res.text)

    print(pay.post_(body='111'.encode('utf-8', 'ignore'), out_trade_no='23232323', total_fee='1', spbill_create_ip=ip,
                  notify_url='api.zgtxcj.com', code=code))
    return Response(code)
