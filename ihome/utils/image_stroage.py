# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_data, etag
import qiniu.config
#需要填写你的 Access Key 和 Secret Key
access_key = 'wbquoVNhFdbuRZI2ECl5SeIa940bJRuKDom92HZO'
secret_key = '3KbHHR8hXa92_hXVJr3kTKc_k428ykwJFRtquccj'
#构建鉴权对象
def storage(file_data):
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = 'ihome-python2'
    #上传后保存的文件名

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)
    #要上传文件的本地路径

    ret, info = put_data(token, None, file_data)
    print(info)
    if info.status_code ==200:
        return ret.get("key")
    else:
        raise  Exception("上传文件失败")



if __name__ == '__main__':
    with open("./1.jpg",'rb') as f:
        file_data = f.read()
        storage(file_data)