import os
import json
import base64

from common.tool.export import ToolBase, TaskConfig, TASK_MANAGE
from common.third_util.io.api import Api
from common.third_util.io.email_util import EmailUtil
from common.third_util.llm.llm_client import LlmClient
from common.util.export import C, time_format, logger, time


class TaskTool(ToolBase):
    def todo_every_day(self, uri, name, mp: dict, **kw):
        date_str = time_format(fmt="%Y-%m-%d")
        api = Api().set_endpoint(uri).set_proxy({"http": None, "https": None})
        ret = []
        for type, values in mp.items():
            for v in values:
                value = dict(title=f"{date_str}_{v}", category=type, content="AUTO_GEN")
                res = api.post(
                    "/app/todo/web_insert",
                    value,
                    headers={C.THE_DEV_USER: name},
                )
                ret.append(res)
                logger.map(type=type, value=value, res=res)
        return ret

    def icbc_import(
        self,
        email_env,
        llm_config,
        sender_email,
        pdf_password="",
        since_date="01-Jan-2026",
        category="money",
        uri=None,
        name=None,
        **kw,
    ):
        import imaplib
        import email as email_lib
        import pdfplumber

        api = None
        if uri and name:
            api = Api().set_endpoint(uri).set_proxy({"http": None, "https": None})

        mail = EmailUtil(email_env)
        client = mail.connect_imap()
        client.select("INBOX")

        result, data = client.search(
            None, f'(FROM "{sender_email}" SINCE {since_date})'
        )
        if result != "OK":
            raise Exception(f"IMAP search failed: {data}")

        msg_ids = data[0].split() if data[0] else []
        if not msg_ids:
            logger.info(f"no emails from {sender_email} since {since_date}")
            mail.close_imap()
            return 0

        latest = msg_ids[-1]
        msg_id = latest.decode()
        logger.info(f"processing latest email: {msg_id}")

        llm = LlmClient(llm_config)
        tmp_dir = "data/tmp"
        os.makedirs(tmp_dir, exist_ok=True)
        imported = 0

        try:
            part_num = self._find_pdf_part(client, latest)
            if not part_num:
                logger.warning(f"no PDF attachment found in email {msg_id}")
                mail.close_imap()
                return 0

            result, att_data = client.fetch(latest, f"(BODY.PEEK[{part_num}])")
            if result != "OK":
                raise Exception(f"failed to fetch attachment part {part_num}")

            raw = att_data[0][1]
            if raw.startswith(b"%PDF"):
                pdf_binary = raw
            else:
                pdf_binary = base64.b64decode(raw)

            pdf_path = os.path.join(tmp_dir, f"{msg_id}.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf_binary)

            text = ""
            with pdfplumber.open(pdf_path, password=pdf_password) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            if not text.strip():
                logger.warning(f"no text extracted from {pdf_path}")
                os.remove(pdf_path)
                mail.close_imap()
                return 0

            prompt = f"""你是一个银行流水解析助手。从以下工商银行流水PDF文本中提取所有交易记录，返回JSON数组，格式：
[{{"title": "日期_摘要", "money": 金额, "content": "备注"}}]

要求：
- title 需唯一标识该笔交易
- money 为数字正数（收入）或负数（支出）
- 只返回纯JSON，不要其他文字

PDF文本：
{text}"""

            llm_result = llm.simple_chat(prompt)
            transactions = self._parse_llm_result(llm_result)

            for tx in transactions:
                title = tx.get("title", str(time.time()))
                todo_value = dict(
                    title=title,
                    category=category,
                    money=tx.get("money", 0),
                    content=tx.get("content", ""),
                )
                if api:
                    res = api.post(
                        "/app/todo/web_insert",
                        todo_value,
                        headers={C.THE_DEV_USER: name},
                    )
                    logger.map(tx=title, res=res)
                else:
                    logger.info(
                        f"dry-run: would insert {title} money={tx.get('money')}"
                    )
                imported += 1

            os.remove(pdf_path)

        except Exception as e:
            logger.error(f"failed to process email {msg_id}: {e}", stack_info=True)
        finally:
            mail.close_imap()

        logger.info(f"icbc_import done, imported {imported} transactions")
        return imported

    @staticmethod
    def _find_pdf_part(client, msg_id) -> int | None:
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
    def _parse_llm_result(text: str) -> list:
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
    TaskTool().run()
