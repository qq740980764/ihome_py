# coding:utf-8
from ihome import db
from ihome.models import User
from ihome.utils.commons import login_requried
from ihome.utils   import constants
from ihome.utils.image_stroage import storage
from . import api
from flask import request, current_app, jsonify, g, json, session
from ihome.utils.response_code import  RET

@api.route("/users/avatar",methods=["POST"])
@login_requried
def portrait():
    """
    #上传头像
    :return:
    """
    user_id = g.user_id
    image_file = request.files.get("avatar")

    #,验证是否存在

    if  image_file is None:
        return jsonify(errno=RET.DATAERR,errmsg="file image  missing")

    file_data = image_file.read()
    #上传图片
    # try:
    avatar_url = storage(file_data)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DATAERR,errmsg="文件上传失败")

    #将数据保存到数据库中
    try:
        User.query.filter_by(id=user_id).update({"avatar_url": avatar_url})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="mysql err")

    avatar_url =constants.QINIU_HTTP+avatar_url
    return jsonify(errno=RET.OK,errmsg="image upload success",data={
        "avatar_url":avatar_url,
    })




@api.route("/user",methods=["GET"])
@login_requried
def get_user_profile():
    """
    #my.html传递信息
    参数:空
    :return:....
    """
    user_id = g.user_id

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="mysql error")

    if  not user:
        return jsonify(errno=RET.NODATA, errmsg="user missing")

    return jsonify(errno=RET.OK, errmsg="OK",data =user.to_dict())



#上传用户名
@api.route("/user/name",methods=["PUT"])
@login_requried
def get_username_profile():
    """
    上传用户名
    参数: name,
    :return:{"errno":RET.XXX,"errmsg":"xxxxxx"}
    """
    user_id = g.user_id
    json_data = request.get_json()
    # print(json_data,"json_data")
    name = json_data.get("name")
    if name is None:
        return jsonify(errno=RET.DATAERR, errmsg="data missing")
    try:
        user = User.query.filter_by(id=user_id).update({"name":name})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.commit()
        return jsonify(errno=RET.DBERR, errmsg="mysql error")

    return jsonify(errno=RET.OK, errmsg="OK")



#查询身份证和名字
@api.route("/user/auth",methods=["GET"])
@login_requried
def check_read_name_and_id_card():
    """
    #查询身份证和名字
    :return:
    """
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="data missing")
    if not user:
        return jsonify(errno=RET.NODATA, errmsg="please write read_name/user_card")
    return jsonify(errno=RET.OK, errmsg="OK",data=user.auth_to_dict())


#上传用户真实名以及身份证号
@api.route("/user/auth",methods=["POST"])
@login_requried
def auth_read_name_and_id_card():
    """
    #上传用户真实名以及身份证号
    :return:
    """
    user_id = g.user_id
    json_data = request.get_json()
    real_name = json_data.get("real_name")
    id_card = json_data.get("id_card")
    if not all([real_name,id_card]):
        return jsonify(errno=RET.DATAERR, errmsg="data missing")

    try:
        user = User.query.filter_by(id=user_id,real_name=None,id_card=None).update({"real_name":real_name,"id_card":id_card})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="mysql error")
    else:
        if user is None:
            return jsonify(errno=RET.DATAERR, errmsg="Insert Only once")

    return jsonify(errno=RET.OK, errmsg="OK")



