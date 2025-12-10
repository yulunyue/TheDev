from common.third_util.selenium_util import SeleniumUtil, By
from common.service.export import Api, API_CONFIG
from common.util.export import logger
import time

USER_CONFIG = API_CONFIG.get("Zb")


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


class WebTool(SeleniumUtil):
    JOB_URL = "https://ui.appen.com.cn/v3/worker-job/21e77e76-372e-49c4-b6f0-edcc35fe0663?businessType=WORK&from=Ii92My93b3JrZXItam9icy90YXNrcy9pbi1wcm9ncmVzcz9wYWdlSW5kZXg9MSZqb2JOYW1lPSZwYWdlU2l6ZT0xMCI%3D&projectId=30c9f72d-c822-4534-9dab-691656d4209f"

    def run(self):
        """
        //*[@id="rc-tabs-1-panel-1"]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/button

        """

        self.get(self.JOB_URL)
        buttons = self.get_element_by_id("rc-tabs-1-panel-1").find_elements(
            By.TAG_NAME, "button"
        )
        for e in buttons:
            if e.text != "执行":
                continue
            logger.info(f"{e.tag_name} {e.text}")

    def login(self):
        self.get_element_by_id("name").send_keys(USER_CONFIG.user_name.get_value())
        self.get_element_by_id("password").send_keys(USER_CONFIG.pass_word.get_value())
        self.get_clickable_by_xpath("button", "submit").click()
        self.wait_url_contains("worker-jobs")


API = ApiZb().load()
WT = WebTool()
