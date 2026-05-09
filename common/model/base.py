from common.util.export import File, logger


class BaseModel:
    def load(self, **kw):
        pass

    def set_data(self, **kw):
        self.kw = kw
        try:
            self.load(**kw)
        except Exception as e:
            raise Exception(e, kw)
        return self

    def __repr__(self) -> str:
        return f"{self.kw}"

    store_file: File = None

    @classmethod
    def get_storge(cls) -> File:
        if cls.store_file is None:
            cls.store_file = File("data/model/store.json").write_if_not_exists(dict())
            logger.info(cls.store_file)
        return cls.store_file

    @classmethod
    def new(cls, key):
        r = cls()
        s = cls.get_storge()
        if not s.has(key):
            r.set_data(**cls.make(key))
            s.set(key, value=r.to_json())
        else:
            r.set_data(**s.get(key))
        return r

    @classmethod
    def make(cls):
        raise NotImplementedError()

    def to_json(self):
        raise NotImplementedError()
