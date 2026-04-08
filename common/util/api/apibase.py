class ApiBase:
    ROUTE_PATH = ""

    def _set_env(self, the_dev_user, **kw):
        self.username = the_dev_user
        return self
