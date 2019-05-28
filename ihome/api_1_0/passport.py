# coding:utf-8
from flask import request,current_app
from flask.json import jsonify
from flask import session
from ihome.models import User
from ihome.utils import constants
from ihome.utils.response_code import  RET
from ihome import redis_store, db
from  sqlalchemy.exc import IntegrityError
from . import api
import re
from werkzeug.security import check_password_hash
@api.route("/user",methods=["POST"])
def register():
    """
    用户注册模块
    :参数：mobile, mobile_code,password,password2
    :return:jsonfiy{"errno":data,
                    “errmsg”:data}
    """
    #获取json数据
    dir_Json = request.get_json()
    mobile = dir_Json.get('mobile')
    mobile_code = dir_Json.get('mobile_code')
    password = dir_Json.get('password')
    password2 = dir_Json.get('password2')



    #判断数据完整性
    if not all([mobile,mobile_code,password,password2]):
        return jsonify(erron=RET.PARAMERR,errmsg="missing data")

    #判断手机号格式
    if not re.match(r'1[345678]\d{9}',mobile):
        return jsonify(erron=RET.DATAERR,errmsg="mobile Incorrect data")

    #判断密码
    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="两次密码不一致")

    #验证手机验证码
    try:
        redis_mobile_code = redis_store.get("mobile_code_%s"%mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(erron=RET.DBERR,errmsg="rediss error")

    if not mobile_code:
        return jsonify(erron=RET.DATAERR,errmsg="missing mobile_code")

    if redis_mobile_code != mobile_code:
        return jsonify(erron=RET.DATAERR,errmsg=" mobile_code error")

    #判断手机是否存在,设置密码
    try:
        user = User(name=mobile,mobile=mobile)
        user.password = password
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(erron=RET.DATAEXIST,errmsg=" data exist ")
    except Exception as e :
        current_app.logger.error(e)
        return jsonify(erron=RET.DBERR, errmsg="mysql error")

    #保存session数据
    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id
    return jsonify(erron=RET.OK, errmsg="register ok ")


#
@api.route("/session",methods=["POST"])
def login():
    """
    #登陆
    :return:
    """
    login_data = request.get_json()
    mobile = login_data.get("mobile")
    password = login_data.get("password")
    ip_address = request.remote_addr
    #判断数据是否完整
    if not all([mobile,password]):
        return jsonify(errno=RET.NODATA,errmsg="missing data")

    #判断手机号是否正确r'1[345678]\d{9}]'
    if not re.match(r'1[34567]\d{9}',mobile):
        return jsonify(errno=RET.DBERR,errmsg="mobile error")

    try:
        ip_address_num = redis_store.get("check_password_num_%s"%ip_address)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if ip_address_num is not None  and   int(ip_address_num)>=constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.DBERR,errmsg="ip num many")

    try:
        user=User.query.filter_by(mobile=mobile).first()
        print(user,'的值是')
    except Exception as e:
        current_app.logger.error(e)

    #如果用户不存在并且密码不正确的话，提示错误
    else:
        if (not user) or (not user.check_password_hash(password)):
            redis_store.incr("check_password_num_%s"%ip_address,1)
            redis_store.expire("check_password_num_%s"%ip_address,constants.IP_NUM_REDIS_EXPIRES)
            return jsonify(errno=RET.NODATA,errmsg="name/password error")

    print(user,'的值是')
    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id
    return jsonify(errno=RET.OK,errmsg="logging ok ")


@api.route("/session", methods=["GET"])
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    name = session.get("name")
    # 如果session中数据name名字存在，则表示用户已登录，否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session",methods=["Delete"])
def delete():
    """
    #删除session
    :return:
    """
    session["name"] = None
    return jsonify(errno=RET.OK,errmsg="user")