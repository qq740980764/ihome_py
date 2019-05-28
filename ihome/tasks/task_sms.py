# coding:utf-8

from celery import Celery

from ihome import redis_store
from ihome.libs.yuntongxun.SendTemplateSMS import Send
from ihome.utils.constants import MOBILE_CODE_REDIS_EXPIRES, MOBILE_REDIS_EXPIRES

celery_app = Celery("ihome2")



@celery_app.task
def send_sms(to, datas, temp_id):
    sms = Send()
    sms.sendTemplatesms(to, datas, temp_id)
    # redis_store.setex("mobile_code_time_%s" % to, MOBILE_REDIS_EXPIRES, 1)
