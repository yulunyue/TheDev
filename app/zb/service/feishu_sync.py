import datetime
import hashlib

from common.third_util.feishu import get_valid_user_token, resolve_node, read_range, write_range
from common.third_util.feishu.drive import download_file, upload_file
from common.util.export import File, logger

from ..model import Fp, ROOT
from .task_packager import OUTPUT_DIR

WIKI_TOKEN = "Szwrwgy6siVYKvksfPWc0g7ynGd"
SHEET_ID = "6cba43"
FEISHU_FILE_URL = "https://uq4mkty1bj.feishu.cn/file"

COL_C = 2
COL_D = 3
COL_E = 4
COL_F = 5
COL_V = 21


class FeishuSync:
    def sync(self, name: str):
        zip_file = OUTPUT_DIR.child(f"{name}.zip")
        if not zip_file.exists():
            logger.warning(f"[feishu_sync] ZIP 不存在: {zip_file.path}")
            return

        local_md5 = hashlib.md5(zip_file.read_data()).hexdigest()

        user_token = get_valid_user_token()
        obj_token, _, _ = resolve_node(WIKI_TOKEN, user_token)

        rows = read_range(obj_token, SHEET_ID, user_token=user_token)
        if not rows:
            logger.warning("[feishu_sync] 表格为空")
            return

        file_token = upload_file(zip_file.path, parent_node=obj_token, parent_type="sheet_file", user_token=user_token)
        logger.info(f"[feishu_sync] ZIP 已上传: {name}.zip token={file_token}")

        target_row_idx, target_row = self._find_row(rows, name)
        qc_text = self._build_qc_summary(name)
        link = {"type": "url", "link": f"{FEISHU_FILE_URL}/{file_token}", "text": f"{name}.zip"}

        if target_row_idx is not None:
            if self._md5_unchanged(target_row, local_md5, user_token):
                logger.info(f"[feishu_sync] 跳过 {name}: MD5 未变")
                return
            self._update_row(obj_token, target_row_idx, link, qc_text, user_token)
            logger.info(f"[feishu_sync] 更新 {name}: row={target_row_idx + 1}")
        else:
            self._insert_row(obj_token, len(rows), link, qc_text, name, user_token)
            logger.info(f"[feishu_sync] 插入 {name}: row={len(rows) + 1}")

    def _find_row(self, rows, name):
        zip_name = f"{name}.zip"
        for i in range(1, len(rows)):
            row = rows[i]
            if len(row) <= COL_D or row[COL_D] != "余伦跃":
                continue
            if len(row) > COL_C and row[COL_C] and isinstance(row[COL_C], list):
                for item in row[COL_C]:
                    if isinstance(item, dict) and item.get("text") == zip_name:
                        return i, row
        return None, None

    def _md5_unchanged(self, row, local_md5, user_token):
        if len(row) <= COL_C:
            return False
        cell = row[COL_C]
        if not cell or not isinstance(cell, list) or len(cell) == 0:
            return False
        item = cell[0]
        file_token = item.get("fileToken") if isinstance(item, dict) else None
        if not file_token:
            return False
        try:
            old_data = download_file(file_token, user_token)
            old_md5 = hashlib.md5(old_data).hexdigest()
            return old_md5 == local_md5
        except Exception:
            return False

    def _update_row(self, obj_token, row_idx, link, qc_text, user_token):
        row_num = row_idx + 1
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        write_range(obj_token, SHEET_ID, f"A{row_num}:A{row_num}", [[ts]], user_token=user_token)
        write_range(obj_token, SHEET_ID, f"C{row_num}:C{row_num}", [[link]], user_token=user_token)
        write_range(obj_token, SHEET_ID, f"E{row_num}:E{row_num}", [[qc_text]], user_token=user_token)
        write_range(obj_token, SHEET_ID, f"F{row_num}:F{row_num}", [["返修完成"]], user_token=user_token)

    def _insert_row(self, obj_token, total_rows, link, qc_text, name, user_token):
        row_num = total_rows + 1
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        new_row = [None] * (COL_V + 1)
        new_row[0] = ts
        new_row[COL_C] = link
        new_row[COL_D] = "余伦跃"
        new_row[COL_E] = qc_text
        new_row[COL_F] = "已完成"
        write_range(obj_token, SHEET_ID, f"A{row_num}:V{row_num}", [new_row], user_token=user_token)

    def _build_qc_summary(self, name):
        root = ROOT.search_one(f"{name}/{Fp.run_verification_py}").parent()
        report_file = root.child(f"{root.name}_qc_report.json")
        if not report_file.exists():
            return "质检报告未生成"

        try:
            report = report_file.read_file()
            if not isinstance(report, dict):
                return "质检报告格式异常"
        except Exception:
            return "质检报告解析失败"

        lines = []
        for module in report.get("modules", []):
            m_name = module.get("name", "")
            if module.get("passed"):
                lines.append(f"{m_name}: pass")
            else:
                err_count = module.get("error_count", 0)
                lines.append(f"{m_name}: {err_count}err")

        overall = report.get("overall", "")
        total_errors = report.get("total_errors", 0)
        if overall == "PASS":
            lines.append("PASS")
        else:
            lines.append(f"FAIL ({total_errors} errors)")

        return "\n".join(lines)
