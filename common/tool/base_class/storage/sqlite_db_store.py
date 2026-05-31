import os
import sqlite3

from ..baseconfig import ConfigBase
from ..base_model import BaseModel
from common.util.export import logger, List, Dict, Self, json, re


_shared_connections: Dict[str, sqlite3.Connection] = {}


class SqliteDbStore(ConfigBase):
    _conn = None
    _config = None
    _table_name = ""

    @classmethod
    def _get_table_name(cls):
        if hasattr(cls, "__table_name__") and cls.__table_name__:
            return cls.__table_name__
        name = cls.__name__
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    @staticmethod
    def _get_sqlite_type(param: BaseModel) -> str:
        name = param.__class__.__name__
        if name == "NumberModel":
            return "REAL"
        elif name == "BoolModel":
            return "INTEGER"
        return "TEXT"

    @staticmethod
    def _serialize_value(key, value, params: Dict[str, BaseModel]):
        if key not in params:
            return value
        name = params[key].__class__.__name__
        if name in ("DictModel", "JsonDictModel", "ListModel"):
            return json.dumps(value, ensure_ascii=False)
        elif name == "BoolModel":
            return 1 if value else 0
        return value

    @staticmethod
    def _deserialize_value(key, value, params: Dict[str, BaseModel]):
        if key not in params or value is None:
            return value
        name = params[key].__class__.__name__
        if name in ("DictModel", "JsonDictModel", "ListModel"):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return {}
        elif name == "BoolModel":
            return bool(value)
        return value

    @classmethod
    def _create_table(cls):
        table = cls._table_name
        cols = ["id TEXT PRIMARY KEY NOT NULL"]
        for key, p in cls.get_params().items():
            cols.append(f"{key} {cls._get_sqlite_type(p)}")
        sql = (
            f"CREATE TABLE IF NOT EXISTS {table} (\n  "
            + ",\n  ".join(cols)
            + "\n) WITHOUT ROWID"
        )
        cls._conn.execute(sql)
        cls._conn.commit()

    @classmethod
    def _upsert_row(cls, idx, data):
        table = cls._table_name
        params = cls.get_params()
        cols = ["id"]
        vals = [idx]
        for k, v in data.items():
            cols.append(k)
            vals.append(cls._serialize_value(k, v, params))
        placeholders = ",".join(["?"] * len(cols))
        sql = (
            f"INSERT OR REPLACE INTO {table} ({','.join(cols)}) VALUES ({placeholders})"
        )
        cls._conn.execute(sql, vals)

    @classmethod
    def init_resource(cls):
        cls._config = dict()
        os.makedirs(os.path.dirname(cls.resource_path), exist_ok=True)
        db_path = cls.resource_path
        if db_path in _shared_connections:
            cls._conn = _shared_connections[db_path]
        else:
            cls._conn = sqlite3.connect(db_path, check_same_thread=False)
            _shared_connections[db_path] = cls._conn
        cls._table_name = cls._get_table_name()
        cls._create_table()
        cls.load_data_from_db()
        return cls.instance_map

    @classmethod
    def close_resource(cls):
        if cls._conn:
            db_path = cls.resource_path
            if db_path in _shared_connections:
                _shared_connections.pop(db_path)
            cls._conn.close()
            cls._conn = None

    @classmethod
    def load_data_from_db(cls):
        cls.instance_map = dict()
        table = cls._table_name
        params = cls.get_params()
        cursor = cls._conn.execute(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            idx = row_dict.pop("id")
            non_null = {}
            for k, v in row_dict.items():
                if v is not None:
                    non_null[k] = cls._deserialize_value(k, v, params)
            cls._config[idx] = non_null
            try:
                instance = cls.new(idx)
                cls.instance_map[idx] = instance
            except Exception as e:
                logger.error(e, stack_info=True)

    @classmethod
    def query(cls, key) -> Self:
        try:
            return cls.instance_map[key]
        except Exception as e:
            raise Exception(e, cls.resource_path)

    @classmethod
    def save_to_local(cls):
        table = cls._table_name
        params = cls.get_params()
        for idx, data in cls._config.items():
            cls._upsert_row(idx, data)
        cls._conn.commit()
        return cls

    def update_param_value(self, ins: BaseModel, value, if_none=False):
        c = self.__class__._config
        if self._id not in c:
            c[self._id] = dict()
        if ins.key in c[self._id] and if_none:
            return
        c[self._id][ins.key] = value
        self.__class__._upsert_row(self._id, c[self._id])
        self.__class__._conn.commit()

    def get_param_value(self, ins: BaseModel):
        if self._id not in self.__class__._config:
            return ins.default_value
        c = self.__class__._config[self._id]
        if ins.key in c:
            return c[ins.key]
        return ins.default_value

    def delete(self):
        table = self.__class__._table_name
        self.__class__._conn.execute(f"DELETE FROM {table} WHERE id=?", (self._id,))
        self.__class__._conn.commit()
        self.__class__.instance_map.pop(self._id)
        self.__class__._config.pop(self._id, None)
        return self

    @classmethod
    def all(cls) -> List[Self]:
        return cls.instance_map.values()
