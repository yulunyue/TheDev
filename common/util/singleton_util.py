class SingletonUtil:
    _instance = None

    @classmethod
    def new(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
