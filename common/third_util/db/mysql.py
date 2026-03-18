import pymysql


class MysqlBackend:
    def load(self, ip, username, password, port, db_name, timeout=5) -> None:
        self.timeout = timeout
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.db_name = db_name
        self._conn = None
        self._cursor = None
        return self

    def begin(self):
        if self._conn:
            self._conn.commit()
            self._conn.close()
        self._conn = None

    def get_conn(self):
        if self._conn is None:

            self._conn = pymysql.connect(
                host=self.ip,
                port=int(self.port),
                password=self.password,
                user=self.username,
                database=self.db_name,
                connect_timeout=3,
            )
        return self._conn

    def get_cursor(self):
        if self._cursor is None:
            self.cursor = self.get_conn().cursor()
        return self.cursor

    def query(self, sql):
        c = self.get_cursor()
        try:
            c.execute(sql)
        except Exception as e:
            self.error(e, sql)
        return c.fetchall()

    def execute(self, sql):
        c = self.get_cursor()
        try:
            c.execute(sql)
            return list(c.fetchall())
        except Exception as e:
            self.error(e, sql)
            return []

    def rollback(self):
        self.get_conn().rollback()
        return self

    def commit(self):
        self.get_conn().commit()
        return self

    def error(self, *args):
        raise Exception(*args)
