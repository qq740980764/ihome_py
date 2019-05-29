# coding:utf-8
import random
from ihome.libs.yuntongxun.SendTemplateSMS import  Send
from flask import current_app, jsonify, make_response, request
# from captcha import captcha
from ihome import redis_store
from ihome.models import User
# from ihome.tasks.task_sms import send_sms
from . import api
from ihome.tasks.sms.tasks import send_sms
from ihome.utils.response_code import  RET
from ihome.utils.constants import  IMAGE_CODE_REDIS_EXPIRES,MOBILE_CODE_REDIS_EXPIRES,MOBILE_REDIS_EXPIRES
from ihome.utils.captcha.captcha import captcha
# import generate_capthcha
@api.route("/image_codes/<image_code_id>")
def image_code_id(image_code_id):
    name, text, image = captcha.generate_captcha()
    try:
        redis_store.setex("image_code_%s"%image_code_id,IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR,errmsg="save image code faill")
    resp = make_response(image)
    resp.headers["Content-Type"] = "image/jpg"
    return resp


@api.route("/sms_codes/<re(r'1[3579]\d{9}'):mobile>")
def mobile_code_Id(mobile):
    image_code_id= request.args.get('imageCodeId')
    image_code  = request.args.get('imageCode')

    if not all([image_code_id,image_code]):
        return jsonify(error=RET.PARAMERR,errmsg="missing data")

    #获取图片验证码
    try:
        redis_image_code=redis_store.get('image_code_%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR,errmsg="redis abnormal")

    if not redis_image_code:
        return jsonify(error=RET.NODATA,errmsg="captcha Invalid")

    #判断图片验证码
    redis_image_code = redis_image_code.lower()
    image_code = image_code.lower()
    if redis_image_code != image_code:
        return jsonify(error=RET.REQERR, errmsg="captcha error")

    #删除图片验证码
    try:
        redis_store.delete('image_code_%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    #判断是否在60秒内
    try:
        mobile_exist=redis_store.get("mobile_code_time_%s"%mobile)
    except  Exception as e :
        current_app.logger.error(e)
    else:
        if mobile_exist:
            return jsonify(error=RET.REQERR,errmsg="Too many queries ")

    #查询手机号是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if not user is None:
            return jsonify(error=RET.NODATA,errmsg="user not data ")

    mobile_code = "%06d" % random.randint(0, 999999)

    #将手机验证码存入redis中
    try:
        redis_store.setex("mobile_code_%s"%mobile,MOBILE_CODE_REDIS_EXPIRES,mobile_code)

        print(mobile_code)
    except Exception as e:
        return jsonify(error=RET.REQERR, errmsg="db error")

    #判断是否发送
    try:
        sms  = Send()
        sms.sendTemplatesms(mobile,[mobile_code,MOBILE_CODE_REDIS_EXPIRES/60],1)
        redis_store.setex("mobile_code_time_%s"%mobile,MOBILE_REDIS_EXPIRES,1)
    except  Exception as e :
        current_app.logger.error(e)
        return jsonify(error=RET.THIRDERR, errmsg="sms send fail")

    # result=send_sms.delay(mobile,[mobile_code,MOBILE_CODE_REDIS_EXPIRES/60],1)
    # #打印celery成功时返回的的值(获取redis成功的值)
    # print(result.get())
    # except  Exception as e :
    #     return jsonify(error=RET.THIRDERR, errmsg="sms send fail")

    #判断是否发送成功

    return jsonify(error=RET.OK, errmsg="sms send ok")



