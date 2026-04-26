class ApiBase:
    ROUTE_PATH = ""

    def _set_env(self, the_dev_user, **kw):
        from app.tool.user import UserModel

        self.username = the_dev_user
        if not UserModel.exist(self.username):
            UserModel.get(self.username).save()
        return self
