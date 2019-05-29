
#coding:utf-8
import time

from CCPRestSDK import REST
# import .ConfigParser

#主帐号
accountSid= '8a216da86898412b0168db9fe94906bc';

#主帐号Token
accountToken= '72a9fafe28314f0ca0e9d25097986624';

#应用Id
appId='8a216da86898412b0168db9fe9ac06c3';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

class Send(object):
    isstance = None
    def __new__(cls):
        if cls.isstance is None:
            obj = super(Send,cls).__new__(cls)

            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.isstance = obj
        return cls.isstance




    def sendTemplatesms(self,to,datas,temp_id):

    
        result = self.rest.sendTemplateSMS(to, datas, temp_id)


        status_code = result.get("statusCode")
        if status_code == "000000":
            # 表示发送短信成功
            return 0
        else:
            # 发送失败
            return -1
    
   
#sendTemplateSMS(手机号码,内容数据,模板Id)
if __name__ == '__main__':
    ccp = Send()


    ret = ccp.sendTemplatesms("13543318443", ["1234", "5"], 1)
    print(ret)
