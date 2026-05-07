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
