from common.third_util.selenium_util import SeleniumUtil, By
from common.util.export import time, logger, File, List
from common.service.export import Api, API_CONFIG
from .model.export import task_cfg, TaskCfg, get_info_by_name, TASK_DIR, CS

USER_CONFIG = API_CONFIG.get("Zb")


class WebTool(SeleniumUtil):
    projectId = "30c9f72d-c822-4534-9dab-691656d4209f"
    fm = "Ii92My93b3JrZXItam9icy90YXNrcy9pbi1wcm9ncmVzcz9wYWdlSW5kZXg9MSZqb2JOYW1lPSZwYWdlU2l6ZT0xMCI%3D"
    main_uri = "https://ui.appen.com.cn/v3/worker-job"

    def __init__(self, repo):
        self.repo = repo
        self.job_id = {
            "lbry-sdk": "144a7a09-bbc2-4527-ad1f-8dc27b83e323",
            "briefcase": "21e77e76-372e-49c4-b6f0-edcc35fe0663",
        }[repo]

    @property
    def JOB_URL(self):
        return f"{self.main_uri}/{self.job_id}?businessType=WORK&from={self.fm}&projectId={self.projectId}"

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

    def get_download_url(self, uri):
        self.get(uri)
        for btn in self.get_elements_by_xpath("//button"):
            if btn.text == "点击下载":
                return btn.get_attribute("url")
        raise Exception(uri)

    def submit(self, t: TaskCfg):
        if not t.zip_file.exists():
            return
        logger.info(t.zip_file)
        _, skip_msg = t.skip()
        self.upload(t.zip_file)
        self.get(t.submit_url.get_value())
        self.reload()
        if skip_msg != CS.SUCCESS:
            self.get_element_by_xpath("//input[@value='invalid']").click()
            inp = self.get_element_by_xpath('//input[@class="ct-ant-input"]')
            inp.clear()
            inp.send_keys(str(skip_msg))
            self.get_element_by_xpath("//div[@class='ant-select-selector']").click()
            time.sleep(1)
            self.get_element_by_xpath("//div[@title='无效数据']").click()
        else:
            self.get_element_by_xpath("//input[@value='valid']").click()
        self.get_element_by_xpath("//button[@form='task-form'][2]").click()
        self.get_element_by_xpath(
            "//div[@class='ant-modal-confirm-btns']//button[1]"
        ).click()

    def upload(self, f: File):
        self.get("http://39.99.159.226")
        self.reload()
        self.get_element_by_xpath("//input[@type='file']").send_keys(f.get_abs_path())
        self.get_element_by_xpath(f"//p[contains(text(),'{f.file_name}')]")
        return True

    def parse_job_table(self):
        for tr in self.get_elements_by_xpath("//tbody[@class='ant-table-tbody']/tr"):
            if not tr.text:
                continue
            task_id, data_batch, statu, data_source, rest_time, method, *args = (
                tr.text.split(" ")
            )
            t = task_cfg(self.repo, task_id)

            self.to_do_task.append(t)
            if not t.submit_url.get_value():
                logger.info(
                    f"任务ID:{task_id} 数据批次:{data_batch} 状态:{statu} 数据来源:{data_source} 剩余时间:{rest_time} 方法:{method}"
                )
                tr.find_element(By.TAG_NAME, "button").click()
                self.switch_to_window()
                t.submit_url.set_value(self.current_url)
                t.down_load_uri.set_value(self.get_download_url(self.current_url))
                t.save()
                self.close_current_window()
                self.switch_to_window(0)
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
        self.to_do_task: List[TaskCfg] = []
        self.get(self.JOB_URL)
        self.reload()
        self.get_job_info()
        for t in self.to_do_task:
            self.submit(t.load())


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
