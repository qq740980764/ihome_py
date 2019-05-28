#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""易盾短信发送接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python2.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY,BUSINESS_ID 为对应申请到的值
    2. $ python smssend.py
"""
__author__ = 'yidun-dev'
__version__ = '0.1-dev'

import hashlib
import json
import random
import time
import urllib
import urllib2


class SmsSendAPIDemo(object):
    """易盾短信发送接口示例代码"""
    API_URL = "https://sms.dun.163yun.com/v2/sendsms"
    VERSION = "v2"


    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
            business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = "4f36336e0dce02af299f4b48f457e18b"
        self.secret_key = "4ab38ca5b9109d98bb4ffbfd84b34e65"
        self.business_id = "600e1829b4df4ee58ced5c48b6c222a2"

    def gen_signature(self, params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return hashlib.md5(buff).hexdigest()

    def send(self, params):
        """请求易盾接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        params["signature"] = self.gen_signature(params)

        try:
            params = urllib.urlencode(params)
            request = urllib2.Request(self.API_URL, params)
            content = urllib2.urlopen(request, timeout=1).read()
            return json.loads(content)
        except Exception, ex:
            print "调用API接口失败:", str(ex)


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "your_business_id"  # 业务ID，易盾根据产品业务特点分配
    api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

    params = {
        "needUp": "false",
        "mobile": "15347460537",
        "templateId": "10084",
        "params": "p1=xx&p2=xx",
        # 国际短信对应的国际编码
        "internationalCode": ""
    }
    ret = api.send(params)
    if ret is not None:
        if ret["code"] == 200:
            taskId = ret["result"]["taskId"]
            print "taskId = %s" % taskId
        else:
            print "ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg'])