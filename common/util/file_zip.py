import os
import zipfile
import shutil
from typing import List


class FileZipMixin:
    path: str

    def zip(self, dst=None, targets=None, ignores=None):
        import zipfile

        if dst is None:
            if not self.path.endswith(".zip"):
                dst = self.path + ".zip"
            else:
                dst = self.path
        dst_file = self.__class__(dst).remove()
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as f:
            if targets is None:
                targets = self.list_tree_file()
            for c in targets:
                if isinstance(c, str):
                    local_path, arc_name, c = self.path + "/" + c, c, self.child(c)
                if c.is_file():
                    local_path, arc_name = c.path, c.file_name
                    print(local_path, arc_name)
                    f.write(local_path, arcname=arc_name)
                else:
                    for d in c.list_tree_file(ignores=ignores):
                        local_path, arc_name = d.path, os.path.relpath(
                            d.path, self.path
                        )
                        f.write(local_path, arcname=arc_name)

        return dst_file

    def unzip(self, dst=None):
        import zipfile

        if dst is None:
            dst = self.path.replace(".zip", "")
        if isinstance(dst, str):
            dst = self.__class__(dst)
        try:
            with zipfile.ZipFile(self.path) as zf:
                for member in zf.namelist():
                    zf.extract(member, path=dst.path)
        except Exception as e:
            raise Exception(e, self.path)
        return dst
