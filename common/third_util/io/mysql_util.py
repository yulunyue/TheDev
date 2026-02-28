from common.util.export import logger, File
from common.tool.export import ConfigBase, StrModel, NumberModel
import pymysql


class MysqlConfig(ConfigBase):
    host = StrModel()
    port = NumberModel()
    username = StrModel()
    password = StrModel()
    db_name = StrModel()


class MysqlUtil:
    def __init__(self, name):
        self.config = MysqlConfig(name).set_resource(f"mysql_{name}")
        self._cursor: pymysql.cursors.Cursor = None
        self._conn: pymysql.Connect = None

    @property
    def cursor(self):
        if self._cursor is None:
            self.conn = pymysql.connect(
                host=self.config.host.get_value(),
                port=self.config.port.get_value(),
                password=self.config.password.get_value(),
                user=self.config.username.get_value(),
                database=self.config.db_name.get_value(),
                connect_timeout=3,
            )
            self._cursor = self.conn.cursor()
        return self._cursor

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
