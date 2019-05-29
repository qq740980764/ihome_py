
# coding:utf-8
from ihome.libs.yuntongxun.SendTemplateSMS import Send
from ihome.tasks.main import celery_app

@celery_app.task
def send_sms(to, datas, temp_id):
    sms = Send()
    return sms.sendTemplatesms(to, datas, temp_id)
    # redis_store.setex("mobile_code_time_%s" % to, MOBILE_REDIS_EXPIRES, 1)