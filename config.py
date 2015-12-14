# coding: utf8

import logging
import logging.config

from db import MySQLDB, SqliteDB

# logging.config.dictConfig(yaml.load(open('config/logging.conf')))


class BaseConfig(object):
    MAX_COPIES_PER_DAY = 10000
    MIN_TOTAL_PRICE = 0.01
    DEBUG = True
    SECRET_KEY = 'dPjal9UWtoQKIbcvdEVafzmehFAO'

    # 是否清除购物车，Development默认不清除购物车数据，方便调试
    CLEAR_CART = True   # Clear Cart or not, for development convenient

    # S3 是否上传
    S3_URL_PREFIX = 'https://s3.cn-north-1.amazonaws.com.cn/'
    S3_BUCKET = 'reformation-dev'

    # 下厨房相关API
    XCF_API_HOST = "inner.reformation.xiachufang.com"
    API_URL = "http://reformation.xiachufang.com/api"

    # 微信 API
    WEICHAT_APPID = 'wx88d4f13a40e2e081'
    WEICHAT_SECRET = 'acddbbdf92ae1d369de26e18217ca340'

    # 数据库是否可以被「物理删除」
    DB_ERASABLE = False

    # Console Log
    LOG_CONSOLE = logging.getLogger('console')

    # 是否模拟外部API
    SIMULATE_EXTERNAL_API = False

    # 是否允许跑测试
    ALLOW_TEST = False
    DEFAULT_USER = False

    # 是否禁用CORS
    CORS = False

    # 文件上传位置, 及允许格式
    UPLOAD_FOLDER = '/data/fileUpload/'  # 末尾必须包含 /
    ALLOWED_EXTENSIONS = set(['jpg'])

    # 是否真的付款
    REAL_CHARGE = False
    # 支付系统参数
    PLUTO_HOST = ""
    PLUTO_PUBLIC_KEY = ""
    PLUTO_SECRET_KEY = ""

    SENTRY_DSN = 'http://b2c0ce7939994ee2b9c8b860eeae53bf:b6ba4d2671bd4da9a62585e391329fe5@sentry.xiachufang.com/10'


class Production(BaseConfig):
    DEBUG = False
    MAX_COPIES_PER_DAY = 2
    MIN_TOTAL_PRICE = 15
    SECRET_KEY = 'production-secret-key'
    DB = MySQLDB('reformation', host='reformation1.cnisyucjawac.rds.cn-north-1.amazonaws.com.cn',
                 port=3306, user='reformation', passwd='B7rnFfjBeqVR')
    S3_BUCKET = 'reformation'

    LOG = logging.getLogger('Production')

    REAL_CHARGE = True
    PLUTO_HOST = "http://pluto.xiachufang.com"
    PLUTO_PUBLIC_KEY = "55ALW79ML8OM7BB4KA41"
    PLUTO_SECRET_KEY = "8DYQ4YJ7SND9WPV274BAXYOVR4E3A2F6"


class Staging(BaseConfig):

    DB = MySQLDB('reformation_staging', host='172.31.3.226',
                 port=3306, user='reformation', passwd='reformation')

    S3_BUCKET = 'staging'

    LOG = logging.getLogger('Staging')

    ALLOW_TEST = True
    DB_ERASABLE = False

    REAL_CHARGE = True

    PLUTO_HOST = "http://pluto.xiachufang.com"
    PLUTO_PUBLIC_KEY = "GU3LPX9UGYYJFQQJXDGZ"
    PLUTO_SECRET_KEY = "HDKI8M67R0B0Z9MJYZCKB6MHC776FRV1"

    API_URL = "http://staging.dev.reformation.xiachufang.com/api"

    # 微信 API
    WEICHAT_APPID = 'wx4c820c511606654b'
    WEICHAT_SECRET = '33d8f0a8811fc36f390a8790c4f24df3'


class Development(BaseConfig):

    DB = MySQLDB('reformation', host='localhost', port=3306, user='reformation', passwd='reformation@12W')
    # DB = SqliteDB('tmp/sqlite_devlopment.db')

    DB_ERASABLE = True

    LOG = logging.getLogger('Development')

    S3_BUCKET = 'reformation-dev'

    SIMULATE_EXTERNAL_API = True
    DEFAULT_USER = True

    CORS = True

    REAL_CHARGE = False

    API_URL = "http://staging.dev.reformation.xiachufang.com/api"


class Testing(BaseConfig):

    DB = SqliteDB('tmp/sqlite_testing.db')
    # DB = MySQLDB('reformation_testing', host='localhost', port=3306, user='reformation', passwd='reformation')

    DB_ERASABLE = True

    LOG = logging.getLogger('Testing')

    SIMULATE_EXTERNAL_API = True

    ALLOW_TEST = True
