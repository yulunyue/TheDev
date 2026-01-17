from common.util.export import File, List

PIP_INSTALL_WITH_NO_DEPENDDS = {}


def pkg_repair(self, pkg: str):
    if not pkg or pkg.startswith("#") or pkg.startswith("-"):
        return
    pkg = pkg.replace("#", ",").replace(";", ",").split(",")[0].replace(" ", "")
    if not pkg:
        return
    pkg_name, *version = pkg.replace("<=", "==").replace(">=", "==").split("=")
    flags = ["python -m pip install"]
    if pkg_name in PIP_INSTALL_WITH_NO_DEPENDDS:
        flags.append("--no-deps")
    flags.append(f'"{pkg}"')
    return " ".join(flags)


def pip_install_setup_cfg(self, set_up_file: File):
    pkgs: List[str] = []
    for section_name, depends in {
        "options": ["install_requires"],
        "options.extras_require": ["runtime", "test"],
    }.items():
        for dp in depends:
            lns = set_up_file.get(section_name, dp, default_value="").split("\n")
            for ln in lns:
                pkg = self.pkg_repair(ln)
                if not pkg:
                    continue
                pkgs.append(pkg)
    return pkgs
