import re

from common.util.export import File, dir_object, logger

from ..model.constants import Fp

OUTPUT_DIR = File("app/zb/check/data")


class TaskPackager:
    def package(self, root: File, instance_json: File):
        z = OUTPUT_DIR.child(f"{root.name}.zip").remove()
        z.zip(targets=[root.child(d) for d in dir_object(Fp, str)] + [instance_json])
        logger.info(z)
        return z

    def fix_files(self, root: File):
        self._fix_run_verification(root)
        self._fix_final_diff(root)

    def _fix_run_verification(self, root: File):
        rv = root.child(Fp.run_verification_py)
        if not rv.exists():
            return
        content = rv.read_file()
        if "code.patch" not in content:
            return
        content = content.replace('"code.patch"', '"final.diff"')
        rv.write_file(content)
        logger.info(f"[package] run_verification.py: code.patch -> final.diff")

    def _fix_final_diff(self, root: File):
        diff_file = root.child("final.diff")
        if not diff_file.exists():
            return
        content = diff_file.read_file()
        if not isinstance(content, str):
            return
        clean = self._clean_diff_content(content)
        if self._diff_contains_test_patch(root, clean):
            code_patch = root.child("code.patch")
            if code_patch.exists():
                code_content = code_patch.read_file()
                if isinstance(code_content, str) and code_content.strip():
                    code_clean = self._clean_diff_content(code_content)
                    diff_file.write_file(code_clean)
                    logger.info(f"[package] final.diff: replaced with code.patch (original contained test.patch overlap)")
                    return
        stripped = len(content.splitlines()) - len(clean.splitlines())
        if stripped or not content.endswith("\n"):
            diff_file.write_file(clean)
            logger.info(f"[package] final.diff: stripped {stripped} non-diff lines, ensured trailing newline")

    def _clean_diff_content(self, content: str) -> str:
        lines = content.splitlines()
        clean_lines = []
        for line in lines:
            if line.startswith("diff --git "):
                clean_lines.append(line)
            elif clean_lines:
                clean_lines.append(line)
        if not clean_lines:
            return content
        return "\n".join(clean_lines) + "\n"

    def _diff_contains_test_patch(self, root: File, diff_content: str) -> bool:
        test_patch_file = root.child("test.patch")
        if not test_patch_file.exists():
            return False
        test_content = test_patch_file.read_file()
        if not isinstance(test_content, str):
            return False
        test_clean = self._clean_diff_content(test_content)
        diff_files = self._extract_diff_files(diff_content)
        test_files = self._extract_diff_files(test_clean)
        if not diff_files or not test_files:
            return False
        return test_files.issubset(diff_files) and self._diff_hunks_overlap(diff_content, test_clean)

    def _extract_diff_files(self, diff_content: str) -> set:
        return set(re.findall(r"^diff --git a/(.*?) b/", diff_content, re.MULTILINE))

    def _diff_hunks_overlap(self, diff_a: str, diff_b: str) -> bool:
        hunks_a = set(re.findall(r"^@@\s.*?@@", diff_a, re.MULTILINE))
        hunks_b = set(re.findall(r"^@@\s.*?@@", diff_b, re.MULTILINE))
        return bool(hunks_a & hunks_b)
