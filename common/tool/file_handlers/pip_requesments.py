from common.util.export import File, List


def pip_install_requirements(self, f: File):
    ret = []
    for ln in f.read_line():
        if not ln or ln.startswith("#"):
            continue
        pkg_install_cmd = self.pkg_repair(ln)
        if pkg_install_cmd:
            ret.append(pkg_install_cmd)
    return ret
