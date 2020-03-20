import pymysql

from libs.orm import patch_model

pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

patch_model()
