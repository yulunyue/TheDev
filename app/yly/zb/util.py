from common.third_util.selenium_util import SeleniumUtil
from common.service.api import Api


class WebTool(SeleniumUtil):
    def __init__(
        self,
        url="https://ui.appen.com.cn/v3/worker-jobs/tasks/in-progress?pageIndex=1&jobName=&pageSize=10",
    ):
        super().__init__(url)


class ApiZb(Api):
    def load(self):
        self.task_name = "SWEBench/任务/发布的-12.3"
        return self

    def download_zip_file(self, name, pr):
        return self.get(
            f"https://sh-eng-dataset-zjk.oss-cn-zhangjiakou.aliyuncs.com/shien_files/{self.task_name}/{name}/{name}-{pr}.zip",
            dict(
                OSSAccessKeyId="LTAI5tB2Etp2wUEVtkT7zckM",
                Signature="4HOEZZj5yA3EbYIGclOQ6DOQqZU",
                Expires=1766157704,
            ),
        )


WT = WebTool()
