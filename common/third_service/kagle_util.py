from kaggle.cli import main
from common.third_util.api import Api
from common.util.log import std_mock


class KagleUtil(Api):
    def get_endpoint(self):
        return "www.kaggle.com"

    def test(self):
        return self.get("/api/v1/competitions/data/download-all/connectx")


if __name__ == "__main__":
    std_mock()
    main()
