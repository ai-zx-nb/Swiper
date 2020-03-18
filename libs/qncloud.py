from qiniu import Auth
from qiniu import put_file
from qiniu import put_data

from swiper import conf

QN_AUTH = Auth(conf.QN_ACCESS_KEY, conf.QN_SECRET_KEY)


def upload_to_qncloud(filepath, filename):
    '''将文件上传到七牛云'''
    # 生成上传 Token, 可以指定过期时间等
    token = QN_AUTH.upload_token(conf.QN_BUCKET, filename, 3600)

    # 要上传文件的本地路径
    put_file(token, filename, filepath)

    # 拼接文件链接
    file_url = '%s/%s' % (conf.QN_BASEURL, filename)
    return file_url


def upload_data_to_qncloud(filename, filedata):
    '''将文件的数据上传到七牛云'''
    # 生成上传 Token, 可以指定过期时间等
    token = QN_AUTH.upload_token(conf.QN_BUCKET, filename, 3600)

    # 要上传文件的本地路径
    put_data(token, filename, filedata)

    # 拼接文件链接
    file_url = '%s/%s' % (conf.QN_BASEURL, filename)
    return file_url
