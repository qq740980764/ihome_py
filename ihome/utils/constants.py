# coding:utf-8
# 图片验证码的redis有效期, 单位：秒
IMAGE_CODE_REDIS_EXPIRES = 180
# 手机号码
MOBILE_CODE_REDIS_EXPIRES = 500

# 手机号码重复验证
MOBILE_REDIS_EXPIRES = 60


# 数据保存时间
IP_NUM_REDIS_EXPIRES = 600


# 登录错误尝试次数
LOGIN_ERROR_MAX_TIMES = 5

#千牛测试域名
QINIU_HTTP="http://dsqz.online/"


#城区缓存的时间为
REDIS_AREA_DATA = 7200


#广告前五个热门订单
HOT_ADVERT_NUM = 5

# 首页房屋数据的Redis缓存时间，单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200


#最热门的五个订单
HOME_PAGE_MAX_HOUSES = 5
