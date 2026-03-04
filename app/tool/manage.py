from common.util.export import Node, b64_code, File, logger, os
from common.tool.export import DomFile, FrontTable, OsUtil, System


class Manage:
    API_ROUTE = "/app/manage"
    UPLOAD_ROOT = File("data/upload").make_dir_if_not_exist(True)

    def post_file(self, files: DomFile, **kw):
        if isinstance(files, dict):
            for file_name, body in files.items():
                logger.map(name=file_name, size=len(body))
                self.UPLOAD_ROOT.child(file_name).write_file(body)
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
        pid_file = File(f"data/proc/{config}.pid")
        if pid_file.exists():
            try:
                OsUtil("kill").run("-9", pid_file.read_file())
            except Exception as e:
                logger.info(e)
        OsUtil("python").system("main.py", config, "2>&1", "&")
        return Node()
