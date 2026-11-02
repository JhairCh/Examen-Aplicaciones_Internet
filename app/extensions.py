from flask_appbuilder import AppBuilder
from flask_appbuilder.utils.legacy import get_sqla_class

SQLA = get_sqla_class()

db = SQLA()
appbuilder = AppBuilder()