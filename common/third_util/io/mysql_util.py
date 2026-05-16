from common.util.export import logger
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
        self._cursor = None
        self._conn = None

    def get_conn(self):
        if self._conn is None:
            self._conn = pymysql.connect(
                host=self.config.host.get_value(),
                port=self.config.port.get_value(),
                password=self.config.password.get_value(),
                user=self.config.username.get_value(),
                database=self.config.db_name.get_value(),
                connect_timeout=3,
            )
        return self._conn

    @property
    def cursor(self):
        if self._cursor is None:
            self._conn = self.get_conn()
            self._cursor = self._conn.cursor()
        return self._cursor

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def execute(self, sql):
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def begin(self):
        if self._conn:
            self._conn.commit()
            self._conn.close()
        self._conn = None

    def commit(self):
        self.get_conn().commit()
        return self

    def rollback(self):
        self.get_conn().rollback()
        return self
