import json
import os
import base64

from common.tool.export import ToolBase
from common.third_util.io.email_util import EmailUtil
from common.third_util.llm.llm_client import LlmClient
from common.util.export import logger


class IcbcTool(ToolBase):
    name = "icbc"

    def import_bank(self, **kw):
        from app.tool.todo import Todo

        email_env = kw["email_env"]
        llm_config = kw["llm_config"]
        sender_email = kw["sender_email"]
        pdf_password = kw.get("pdf_password", "")
        since_date = kw.get("since_date", "01-Jan-2026")
        category = kw.get("category", "money")
        name = kw["name"]

        mail = EmailUtil(email_env)
        client = mail.connect_imap()
        client.select("INBOX")

        try:
            pdf_path = self._fetch_latest_pdf(client, sender_email, since_date)
            if not pdf_path:
                return 0

            text = self._extract_pdf_text(pdf_path, pdf_password)
            if not text:
                os.remove(pdf_path)
                return 0

            llm = LlmClient(llm_config)
            transactions = self._parse_transactions_via_llm(llm, text)
            os.remove(pdf_path)

            items = [
                dict(
                    title=tx.get("title", ""),
                    category=category,
                    money=tx.get("money", 0),
                    content=tx.get("content", ""),
                    user_id=name,
                )
                for tx in transactions
            ]
            result = Todo().web_batch_insert(items=items)
            logger.info(f"icbc import done, inserted {result}")
            return len(items)

        except Exception as e:
            logger.error(f"icbc import failed: {e}", stack_info=True)
            return 0
        finally:
            mail.close_imap()

    def _fetch_latest_pdf(self, client, sender_email, since_date):
        result, data = client.search(
            None, f'(FROM "{sender_email}" SINCE {since_date})'
        )
        if result != "OK":
            raise Exception(f"IMAP search failed: {data}")

        msg_ids = data[0].split() if data[0] else []
        if not msg_ids:
            logger.info(f"no emails from {sender_email} since {since_date}")
            return None

        latest = msg_ids[-1]
        msg_id = latest.decode()
        logger.info(f"processing latest email: {msg_id}")

        part_num = self._find_pdf_part(client, latest)
        if not part_num:
            logger.warning(f"no PDF attachment in email {msg_id}")
            return None

        result, att_data = client.fetch(latest, f"(BODY.PEEK[{part_num}])")
        if result != "OK":
            raise Exception(f"failed to fetch attachment part {part_num}")

        raw = att_data[0][1]
        pdf_binary = base64.b64decode(raw) if not raw.startswith(b"%PDF") else raw

        tmp_dir = "data/tmp"
        os.makedirs(tmp_dir, exist_ok=True)
        pdf_path = os.path.join(tmp_dir, f"{msg_id}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_binary)
        return pdf_path

    def _extract_pdf_text(self, pdf_path, pdf_password):
        import pdfplumber

        text = ""
        with pdfplumber.open(pdf_path, password=pdf_password) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if not text.strip():
            logger.warning(f"no text extracted from {pdf_path}")
            return ""
        return text

    def _parse_transactions_via_llm(self, llm, text):
        prompt = f"""你是一个银行流水解析助手。从以下工商银行流水PDF文本中提取所有交易记录，返回JSON数组，格式：
[{{"title": "YYYY-MM-DD HH:MM:SS_摘要", "money": 金额, "content": "备注"}}]

要求：
- title 格式：交易日期时间_交易摘要（如 2026-05-20 14:30:00_工资），包含时分秒确保唯一
- money 为数字正数（收入）或负数（支出）
- 只返回纯JSON，不要其他文字

PDF文本：
{text}"""

        result = llm.simple_chat(prompt)
        return self._parse_llm_result(result)

    @staticmethod
    def _find_pdf_part(client, msg_id):
        for part_num in range(1, 10):
            try:
                result, data = client.fetch(msg_id, f"(BODY.PEEK[{part_num}]<0.64>)")
                if result != "OK":
                    continue
                raw = data[0][1] if isinstance(data[0], tuple) else data[0]
                if not raw:
                    continue
                try:
                    decoded = base64.b64decode(raw)
                    if decoded.startswith(b"%PDF"):
                        return part_num
                except Exception:
                    if raw.startswith(b"%PDF"):
                        return part_num
            except Exception:
                continue
        return None

    @staticmethod
    def _parse_llm_result(text):
        text = text.strip()
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end != -1:
            text = text[start : end + 1]
        try:
            data = json.loads(text)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            logger.error(f"failed to parse LLM result: {text[:500]}")
        return []


if __name__ == "__main__":
    IcbcTool().run()
