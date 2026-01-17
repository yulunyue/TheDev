from common.third_util.selenium_util import SeleniumUtil, By, WebElement, File
from common.util.export import time, logger, File, List

from .model.export import new_one, TaskCfg, get_info_by_name, TASK_DIR, CS
from .tool.task_base import ZbTask


class WebTool(SeleniumUtil):
    projectId = "30c9f72d-c822-4534-9dab-691656d4209f"
    fm = "Ii92My93b3JrZXItam9icy90YXNrcy9pbi1wcm9ncmVzcz9wYWdlSW5kZXg9MSZqb2JOYW1lPSZwYWdlU2l6ZT0xMCI%3D"
    main_uri = "https://ui.appen.com.cn/v3/worker-job"
    job_map = dict(
        # zb4="144a7a09-bbc2-4527-ad1f-8dc27b83e323",
        zb3="21e77e76-372e-49c4-b6f0-edcc35fe0663",
    )

    def get_job_url(self, key):
        return f"{self.main_uri}/{self.job_map[key]}?businessType=WORK&from={self.fm}&projectId={self.projectId}"

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
        can_submit = t.can_submit()
        if not can_submit:
            logger.info(f"not can submit {t.zip_file}")
            return
        err_msg = t.error_msg.get_value()
        # if not err_msg.startswith(CS.SKIPPED):
        #     return
        ZbTask().build(t).load().local_cfg.zip()
        logger.info(f"upload {t.zip_file}")
        self.upload(t.zip_file)
        self.get(t.submit_url.get_value())
        self.reload()

        if not err_msg.startswith(CS.SUCCESS):
            self.get_element_by_xpath("//input[@value='invalid']").click()
            inp = self.get_element_by_xpath('//input[@class="ct-ant-input"]')
            inp.clear()
            inp.send_keys(str(t.error_msg.get_value()))
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
        self.get_element_by_xpath("//label[@data-baseweb='radio'][2]").click()
        self.get_element_by_xpath("//input[@type='file']").send_keys(f.get_abs_path())
        self.get_element_by_xpath(f"//p[contains(text(),'{f.file_name}')]")
        return True

    def get_tables(self) -> List[WebElement]:
        tbs = []
        for tr in self.get_elements_by_xpath("//tbody[@class='ant-table-tbody']/tr"):
            if not tr.text:
                continue
            tx = tr.text.split(" ")
            if len(tx) < 4:
                continue
            tbs.append(tr)
        return tbs

    def get_all_tables(self):
        for _ in range(10):
            tables = self.get_tables()
            if tables:
                return tables
            time.sleep(1)
        raise Exception("gg")

    def parse_job_table(self):
        for tr in self.get_all_tables():
            task_id, data_batch, statu, data_source, rest_time, method, *args = (
                tr.text.split(" ")
            )
            if task_id in self.store_task:
                continue
            t = new_one(task_id)
            self.store_task[task_id] = t
            logger.info(
                f"任务ID:{task_id} 数据批次:{data_batch} 状态:{statu} 数据来源:{data_source} 剩余时间:{rest_time} 方法:{method}"
            )
            if not t.submit_url.get_value():
                tr.find_element(By.TAG_NAME, "button").click()
                self.switch_to_window()
                t.set_uri(
                    self.current_url, self.get_download_url(self.current_url), task_id
                )
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

    def get_all_task(self):
        self.store_task = dict()
        for key, v in self.job_map.items():
            self.JOB_URL = self.get_job_url(key)
            self.get(self.JOB_URL)
            self.reload()
            self.get_job_info()
        return self.store_task

    def submit_all(self):
        for key, v in self.get_all_task().items():
            self.submit(v)
