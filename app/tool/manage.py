from common.util.export import Node, md5, b64_code, File, logger, base64_decode, IO_MANAGE, C
import subprocess
import os
from common.tool.export import (
    DomFile,
    FrontTable,
    FontSearch,
    ProcessLock,
)


class Manage:
    UPLOAD_ROOT = File("data/upload").make_dir_if_not_exist(True)

    def post_file(self, files: DomFile, **kw):
        fps = []
        for file_name, body in files.items():
            f = self.UPLOAD_ROOT.child(file_name).write_file(body)
            logger.map(name=file_name, size=len(body), f=f)
            fps.append(f.get_abs_path())
        return Node(value=fps)

    B64_TMP_DATA_MAP = dict()

    def post_files_base64(self, path, data, cur_idx, last_idx):
        f = File(path)
        if cur_idx == 0:
            f.remove()
            self.B64_TMP_DATA_MAP[path] = ""
        self.B64_TMP_DATA_MAP[path] += data
        if cur_idx == last_idx:
            f.write_file(base64_decode(self.B64_TMP_DATA_MAP[path]))
        return Node(
            value=dict(
                value=cur_idx,
                all_size=len(self.B64_TMP_DATA_MAP[path]),
                md5_check=md5(self.B64_TMP_DATA_MAP[path]),
            ),
        )

    def query(self, **kw):
        ft = FrontTable().set_header("path", "update_time", "size")
        for f in self.UPLOAD_ROOT.list_tree_file():
            ft.append_row(
                path=f.path, update_time=f.get_m_time_str(), size=f.get_size()
            )
        return ft

    def unzip(self, path):
        f = File(path)
        f.unzip("./")
        return Node()

    def restart(self, config: str):
        lock = ProcessLock(config)
        lock.kill_old()
        subprocess.Popen(
            ["python", "main.py", config],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        return Node()

    def send_msg(self, topic: str, value: dict, **kw):
        """
        透传消息到指定 topic
        
        :param topic: 目标 topic 名称
        :param value: 消息内容
        """
        IO_MANAGE.send(topic, value)
        return Node(value=value)

    def get_qt_show_config(self, **kw):
        """
        获取 Qt 显示配置
        """
        f = File("config/setting/qt_show.json")
        if f.exists():
            return Node(value=f.read_file())
        return Node(value={"show_keys": []})

    def update_qt_show_config(self, **kw):
        """
        更新 Qt 显示配置并推送
        """
        f = File("config/setting/qt_show.json")
        config = f.read_file() if f.exists() else {"show_keys": []}
        IO_MANAGE.send(C.TOPIC_QT_CONFIG_UPDATE, config)
        return Node(value=config)
