# coding: utf-8
import requests
import time

from base import smart_str, random_str, calculate_sign, dict_to_xml, post_xml, xml_to_dict, format_url

OAUTH2_AUTHORIZE_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?%s"
OAUTH2_ACCESS_TOKEN_URL = "https://api.weixin.qq.com/sns/oauth2/access_token?%s"


class WeiXinPay(object):
    def __init__(self, app_id, mch_id, api_key):
        self.appid = app_id  # 微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
        self.mch_id = mch_id  # 受理商ID，身份标识
        self.api_key = api_key  # 商户支付密钥Key。审核通过后，在微信发送的邮件中查看
        self.common_params = {
            "appid": self.appid,
            "mch_id": self.mch_id,
        }
        self.params = {}
        self.url = ""
        self.trade_type = ""

    def set_params(self, **kwargs):
        self.params = {}
        for (k, v) in kwargs.items():
            self.params[k] = smart_str(v)
        self.params["nonce_str"] = random_str(32)
        if self.trade_type:
            self.params["trade_type"] = self.trade_type
        self.params.update(self.common_params)

    def post_xml(self):
        sign = calculate_sign(self.params, self.api_key)
        xml = dict_to_xml(self.params, sign)
        response = post_xml(self.url, xml)
        return xml_to_dict(response.text)


class UnifiedOrderPay(WeiXinPay):
    """发送预支付单"""

    def __init__(self, appid, mch_id, api_key):
        super(UnifiedOrderPay, self).__init__(appid, mch_id, api_key)
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

    def post(self, body, out_trade_no, total_fee, spbill_create_ip, notify_url, **kwargs):
        tmp_kwargs = {
            "body": body,
            "out_trade_no": out_trade_no,
            "total_fee": total_fee,
            "spbill_create_ip": spbill_create_ip,
            "notify_url": notify_url,
        }
        tmp_kwargs.update(**kwargs)
        self.set_params(**tmp_kwargs)
        return self.post_xml()[1]


class JsAPIOrderPay(UnifiedOrderPay):
    """H5页面的Js调用类"""

    def __init__(self, appid, mch_id, api_key, app_secret):
        super(JsAPIOrderPay, self).__init__(appid, mch_id, api_key)
        self.app_secret = app_secret
        self.trade_type = "JSAPI"

    def create_oauth_url_for_code(self, redirect_uri):
        url_params = {
            "appid": self.appid,
            "redirect_uri": redirect_uri,  # 一般是回调当前页面
            "response_type": "code",
            "scope": "snsapi_base",
            "state": "STATE#wechat_redirect"
        }
        url = format_url(url_params)
        return OAUTH2_AUTHORIZE_URL % url

    def _create_oauth_url_for_openid(self, code):
        url_params = {
            "appid": self.appid,
            "secret": self.app_secret,
            "code": code,
            "grant_type": "authorization_code",
        }
        url = format_url(url_params)
        return OAUTH2_ACCESS_TOKEN_URL % url

    def _get_oauth_info(self, code):
        """
        获取OAuth2的信息：access_token、expires_in、refresh_token、openid、scope
        返回结果为字典，可使用["xxx"]或.get("xxx", None)的方式进行读取
        """
        url = self._create_oauth_url_for_openid(code)
        response = requests.get(url)
        return response.json() if response else None

    def _get_openid(self, code):
        oauth_info = self._get_oauth_info(code)
        if oauth_info:
            return oauth_info.get("openid", None)
        return None

    def _get_json_js_api_params(self, prepay_id):
        js_params = {
            "appId": self.appid,
            "timeStamp": "%d" % time.time(),
            "nonceStr": random_str(32),
            "package": "prepay_id=%s" % prepay_id,
            "signType": "MD5",
        }
        js_params["paySign"] = calculate_sign(js_params, self.api_key)
        return js_params

    def post_(self, body, out_trade_no, total_fee, spbill_create_ip, notify_url, code):
        if code:
            open_id = self._get_openid(code)
            if open_id:
                # 直接调用基类的post方法查询prepay_id，如果成功，返回一个字典
                unified_order = super(JsAPIOrderPay, self).post(body, out_trade_no, total_fee, spbill_create_ip,
                                                                notify_url, open_id=open_id)
                if unified_order:
                    prepay_id = unified_order.get("prepay_id", None)
                    if prepay_id:
                        return self._get_json_js_api_params(prepay_id)
        return None
