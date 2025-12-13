from common.third_util.selenium_util import SeleniumUtil, By
from common.util.export import time, logger
from common.service.export import Api, API_CONFIG
from .util import task_cfg, TaskCfg, get_info_by_name

USER_CONFIG = API_CONFIG.get("Zb")


class WebTool(SeleniumUtil):
    JOB_URL = "https://ui.appen.com.cn/v3/worker-job/21e77e76-372e-49c4-b6f0-edcc35fe0663?businessType=WORK&from=Ii92My93b3JrZXItam9icy90YXNrcy9pbi1wcm9ncmVzcz9wYWdlSW5kZXg9MSZqb2JOYW1lPSZwYWdlU2l6ZT0xMCI%3D&projectId=30c9f72d-c822-4534-9dab-691656d4209f"

    def get_job_info(self):
        self.get(self.JOB_URL)
        if self.parse_job_table():
            self.get_job_info()
        else:
            next_btn = self.get_element_by_xpath("//li[@title='下一页']/button")
            if next_btn.get_attribute("disabled") is not None:
                return
            next_btn.click()
            time.sleep(1)
            self.get_job_info()

    def get_task_info(self, uri, upload_uri):
        self.get(uri)
        btn_upload = None
        ret = None
        for btn in self.get_elements_by_xpath("//button"):
            if btn.text == "点击下载":
                ret = btn.get_attribute("url")
            elif btn.text == "点击上传":
                btn_upload = btn
        if not upload_uri:
            btn_upload.click()
            self.switch_to_window()
            upload_uri = self.current_url
            self.close_current_window()
            self.switch_to_window(0)
        return ret, upload_uri

    def parse_job_table(self):
        for tr in self.get_elements_by_xpath("//tbody[@class='ant-table-tbody']/tr"):
            task_id, data_batch, statu, data_source, rest_time, method, *args = (
                tr.text.split(" ")
            )
            t = task_cfg(task_id=task_id)
            if not t.submit_url.get_value():
                logger.info(
                    f"任务ID:{task_id} 数据批次:{data_batch} 状态:{statu} 数据来源:{data_source} 剩余时间:{rest_time} 方法:{method}"
                )
                tr.find_element(By.TAG_NAME, "button").click()
                self.switch_to_window()
                t.submit_url.set_value(self.current_url)
                self.close_current_window()
                self.switch_to_window(0)
                t.save()
                time.sleep(1)
                self.get_job_info()
                return True
        return False

    def login(self):
        self.get_element_by_id("name").send_keys(USER_CONFIG.user_name.get_value())
        self.get_element_by_id("password").send_keys(USER_CONFIG.pass_word.get_value())
        self.get_clickable_by_xpath("button", "submit").click()
        self.wait_url_contains("worker-jobs")
        return self

    def run(self):
        self.get_job_info()


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


API = ApiZb().load()

WT = WebTool()
