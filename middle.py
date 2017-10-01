# coding: utf-8
from base import smart_str, random_str, calculate_sign, dict_to_xml, post_xml, xml_to_dict


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
        print(self.params)
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
