from common.util.export import Node, md5, b64_code, File, logger, base64_decode, subprocess, os
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
