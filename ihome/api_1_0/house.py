# coding:utf-8
from flask import request, current_app, json, g
from flask.json import jsonify
from flask import session
from sqlalchemy import JSON
from datetime import datetime
from ihome.models import User, Area, House, Facility, HouseImage, Order
from ihome.utils import constants
from ihome.utils.commons import login_requried
from ihome.utils.image_stroage import storage
from ihome.utils.response_code import  RET
from ihome import redis_store, db
from  sqlalchemy.exc import IntegrityError
from . import api
import re

#城区信息
@api.route("/areas")
def seach_name():
    """
    城区信息
    无接受参数
    :return: 返回由列表组成的城区消息
    """
    #判断redis是是否由缓存
    try:
        redis_rea_lst = redis_store.get("area_info")
        # print("redis_rea_lst value is",redis_rea_lst)

    except Exception as e:
        redis_rea_lst = None
        current_app.logger.error(e)
    else:
        # print(redis_rea_lst)

        # redis_dict= json.loads(redis_rea_lst)
        # print(redis_dict)
        if redis_rea_lst:
            return redis_rea_lst, 200, {"Content-Type": "application/json"}
    #查询城区数量
    try:
        area = Area.query.filter()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="mysql error")

    area_lst = []
    for data in area:
        area_lst.append(data.to_dict())

    redis_dict = dict(errno=RET.OK,errmsg="ok",data=area_lst)
    redis_rea_lst = json.dumps(redis_dict)
    try:
        # print("redis_rea_lst",redis_rea_lst)
        redis_store.setex("area_info",constants.REDIS_AREA_DATA,redis_rea_lst)
    except Exception as e:
        current_app.logger.error(e)

    return redis_rea_lst,200,{"Content-Type": "application/json"}


@api.route("/house/info",methods=["POST"])
@login_requried
def release_new_houseing_sources():
    """保存房屋的基本信息
    :accept:
    {
        "title":"",
        "price":"",
        "area_id":"1",
        "address":"",
        "room_count":"",
        "acreage":"",
        "unit":"",
        "capacity":"",
        "beds":"",
        "deposit":"",
        "min_days":"",
        "max_days":"",
        "facility":["7","8"]
    }
    :return:
    """
    user_id = g.user_id
    accept_json = request.get_json()
    title  = accept_json.get("title")
    price  = accept_json.get("price")
    area_id  = accept_json.get("area_id")
    address  = accept_json.get("address")
    room_count  = accept_json.get("room_count")
    acreage  = accept_json.get("acreage")
    unit  = accept_json.get("unit")
    capacity  = accept_json.get("capacity")
    beds  = accept_json.get("beds")
    deposit  = accept_json.get("deposit")
    min_days  = accept_json.get("min_days")
    max_days  = accept_json.get("max_days")


    if not all([title,price,area_id,address,room_count,acreage,unit,capacity,beds,deposit,min_days,max_days]):
        return jsonify(errno=RET.DATAERR,errmsg="data missing")
    try:
        price = float(price)*100
        deposit = float(deposit)*100

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="data missing")

    #判断城区ID是否存在
    try:
        area = Area.query.get(area_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="Mysql Error")
    if not area:
        return jsonify(errno=RET.NODATA,errmsg="No Data")

    # 保存房屋信息
    house = House(user_id=user_id,
                 area_id=area_id,
                 title=title,
                 price=price,
                 address=address,
                 room_count=room_count,
                 acreage=acreage,
                 unit=unit,
                 capacity=capacity,
                 beds=beds,
                 deposit=deposit,
                 min_days=min_days,
                 max_days=max_days,
                 )
    facility = accept_json.get("facility")

    if facility:
        try:
            facility=Facility.query.filter(Facility.id.in_(facility)).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="Mysql Error")
        if not facility:
            return jsonify(errno=RET.NODATA, errmsg="Data Not Exist")

    if facility:
        house.facilities= facility

    #提交数据到Mysql
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="Mysql Data Commit Error")

    return jsonify(errno=RET.OK, errmsg="OK",data={"house_id":house.id})

    
@api.route("/house/image",methods=["POST"])
@login_requried
def upload_pictures():
    """
    上传图片
    :accept:{"house_id":house_id}
    :return:ok
    """
    # accept_json = request.get_json()
    img = request.files.get("house_image")
    house_id= request.form.get("house_id")


    if not all([house_id,img]):

        return jsonify(errno=RET.NODATA,errmsg="data missing")

    #判断house_id真实
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="Mysql Error")
    # print(house,"househouse")
    if not house:
        return jsonify(errno=RET.DATAERR,errmsg="Data Error")

    file_data = img.read()

    #上传图片到千牛
    try:
        url = storage(file_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="Thirde Error")

    house_img = HouseImage(house_id=house_id,url=url)
    db.session.add(house_img)

    if not house.index_image_url:
        house.index_image_url = url
        db.session.add(house)

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="Commit fail")
    url = constants.QINIU_HTTP+url
    return jsonify(errno=RET.OK,errmsg="OK",data = {"image_url":url})




@api.route("/user/house",methods=["GET"])
@login_requried
def my_house_sources():
    """
    发布新房源
    accept:None
    :return: JSON
    """
    user_id = g.user_id

    try:
        # House.query.filter_by(user_id=user_id)
        user = User.query.get(user_id)
        houses = user.houses
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取数据失败")

    # 将查询到的房屋信息转换为字典存放到列表中
    houses_list = []
    if houses:
        for house in houses:
            houses_list.append(house.to_basic_dict())
    return jsonify(errno=RET.OK, errmsg="OK", data={"houses": houses_list})



@api.route("/house/index",methods=["GET"])
def send_index_data():
    """
     获取主页幻灯片展示的房屋基本信息

    :return:
    """
    try:
        ret = redis_store.get("home_page_data")
    except Exception as e:
        current_app.logger.error(e)
        ret = None

    if ret:
        current_app.logger.info("hit house index info redis")
        # 因为redis中保存的是json字符串，所以直接进行字符串拼接返回
        return '{"errno":0, "errmsg":"OK", "data":%s}' % ret, 200, {"Content-Type": "application/json"}
    else:
        try:
            # 查询数据库，返回房屋订单数目最多的5条数据
            houses = House.query.order_by(House.order_count.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

        if not houses:
            return jsonify(errno=RET.NODATA, errmsg="查询无数据")

        houses_list = []
        for house in houses:
            # 如果房屋未设置主图片，则跳过
            if not house.index_image_url:
                continue
            houses_list.append(house.to_basic_dict())

        # 将数据转换为json，并保存到redis缓存
        json_houses = json.dumps(houses_list)  # "[{},{},{}]"
        try:
            redis_store.setex("home_page_data", constants.HOME_PAGE_DATA_REDIS_EXPIRES, json_houses)
        except Exception as e:
            current_app.logger.error(e)
        print(json_houses,"json_houses")
        return '{"errno":0, "errmsg":"OK", "data":%s}' % json_houses, 200, {"Content-Type": "application/json"}


@api.route("/house/<int:house_id>",methods=["GET"])
def get_house_detail(house_id):
    """
    获取详情页，如果时房主为1，不是为-1
    :param house_id:房间号的详情页
    :return:
    """
    user_id = session.get("user_id",-1)


    if not house_id:
        return jsonify(error=RET.NODATA,errmsg="Data missing")


    try:
        ret = redis_store.get("house_info_%s"%house_id)
    except Exception as e:
        current_app.logger.error(e)
        ret = None
    if ret:
        current_app.logger.error("detail_house info redis")
        resp = '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "house":%s}}' % (user_id, ret), \
               200, {"Content-Type": "application/json"}
        return resp

    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg="DB Error")

    if not house:
        return jsonify(error=RET.DBERR, errmsg="house missing")

    try:
        house_data = house.to_full_dict()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg="Redis Error")
    house_json = json.dumps(house_data)

    try:
        redis_store.setex("house_info_%s"%house_id,constants.HOME_PAGE_DATA_REDIS_EXPIRES,house_json)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg="Redis Error")

    resp = '{"error":0,"errmsg":ok,"data":{"house":%s,"user_id":%s}}'%(house_json,user_id),200,{"Content-Type":"application/json"}
    return resp



@api.route("/house/search",methods=["GET"])
def search_house():
    area_id = request.args.get("aid",)
    start_data = request.args.get("sd",)
    end_data = request.args.get("ed",)
    sort_key = request.args.get("sort-key",)
    page = request.args.get("page",)

    if area_id:
        try:
            area = Area.query.get(area_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DATAERR, errmsg="data errer ")




    #处理页数
    try:
        page = int(page)

    except Exception as e:
        current_app.logger.error(e)
        page =1

    filter_params = []


    try:
        if start_data:
            start_data = datetime.strptime(start_data,"%Y-%m-%d")

        if end_data:
            end_data = datetime.strptime(end_data,"%Y-%m-%d")

        if start_data>end_data:
            return jsonify(errno=RET.DATAERR,errmsg="data is errer")

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="data errer ")


    #过滤参数容器
    filter_params = []
    #订单不符合列表
    order_conflict = None
    try:

        if end_data and start_data:
            order_conflict = Order.query.filter(Order.end_date>=start_data and Order.start_date<=end_data).all()
        if start_data:
            order_conflict = Order.query.filter(Order.end_date>=start_data).all()

        if end_data:
            order_conflict = Order.query.filter(Order.start_date<=end_data)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="mysql errer ")

    if order_conflict:
        conflict_house_ids = [conflict.id for conflict in  order_conflict]

        if conflict_house_ids:
            filter_params.append(House.id.notin_(conflict_house_ids))

    if area:
        filter_params.append(area)


    if sort_key =="booking":
        House.query.filter(*filter_params).order_by(House.order_count)

    elif sort_key=="price-inc":
        House.query.filter(*filter_params).order_by(House.price)

    elif sort_key =="price-des":
        House.query.filter(*filter_params).order_by(-House.price)

    else:
        House.query.filter(*filter_params).order_by(House.update_time)
    







