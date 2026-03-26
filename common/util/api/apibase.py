class ApiBase:
    ROUTE_PATH = ""

    def set_env(self, the_dev_user, **kw):
        self.username = the_dev_user
        return self
