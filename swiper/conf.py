'''
程序自身业务配置 和 第三方平台配置
'''

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 7,
    # 'password': None
}

# 云之讯配置
YZX_API = 'https://open.ucpaas.com/ol/sms/sendsms'
YZX_VCODE_ARGS = {
    'appid': '081502fffccd4313bdf6369d36802fd0',
    'sid': 'e749e99071ee277991c27cf9eb62fc8d',
    'token': 'bdcacd327c23b7c6a55adf2955e93c43',
    'templateid': '421727',
    'mobile': None,
    'param': None,
}

# 七牛云配置
QN_ACCESS_KEY = 'kEM0sRR-meB92XU43_a6xZqhiyyTuu5yreGCbFtw'
QN_SECRET_KEY = 'QxTKqgnOb_UVldphU261qu9IdzmjkgGHh6GQVPPy'
QN_BUCKET = 'sh1907'
QN_BASEURL = 'http://q72oz03h1.bkt.clouddn.com'
