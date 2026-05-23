import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header, decode_header
from email.parser import Parser
from email.utils import parsedate_to_datetime
import json
import poplib

from common.tool.export import FileConfig, StrModel, NumberModel
from common.util.export import File, logger, Node


class EmailConfig(FileConfig):
    username = StrModel()
    password = StrModel()
    smtp_host = StrModel()
    smtp_port = StrModel(default_value="465")
    imap_host = StrModel()
    imap_port = StrModel(default_value="993")
    sender = StrModel()
    use_ssl = StrModel(default_value="1")


EmailConfig.set_resource("config/setting/email.json")


def _decode_email_header(value):
    if value is None:
        return ""
    decoded_parts = decode_header(value)
    parts = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            try:
                parts.append(part.decode(charset or "utf-8", errors="replace"))
            except Exception:
                parts.append(part.decode("utf-8", errors="replace"))
        else:
            parts.append(part)
    return " ".join(parts)


def _get_email_body(msg):
    body = ""
    html = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    charset = part.get_content_charset() or "utf-8"
                    body += part.get_payload(decode=True).decode(charset, errors="replace")
                except Exception:
                    pass
            elif content_type == "text/html":
                try:
                    charset = part.get_content_charset() or "utf-8"
                    html += part.get_payload(decode=True).decode(charset, errors="replace")
                except Exception:
                    pass
    else:
        try:
            charset = msg.get_content_charset() or "utf-8"
            body = msg.get_payload(decode=True).decode(charset, errors="replace")
        except Exception:
            body = str(msg.get_payload())
    return body or html, html


def _get_attachments(msg):
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            filename = part.get_filename()
            if filename:
                filename = _decode_email_header(filename)
                attachments.append({
                    "filename": filename,
                    "content_type": part.get_content_type(),
                    "size": len(part.get_payload(decode=True) or b""),
                })
    return attachments


class EmailUtil:
    def __init__(self, env_name) -> None:
        self.smtp_client: smtplib.SMTP = None
        self.imap_client: imaplib.IMAP4 = None
        self.env_name = env_name
        self.config = EmailConfig.get(env_name)

    # --- SMTP ---

    def connect_smtp(self):
        if self.smtp_client is None:
            use_ssl = self.config.use_ssl.get_value() == "1"
            host = self.config.smtp_host.get_value()
            port = int(self.config.smtp_port.get_value())
            if use_ssl:
                self.smtp_client = smtplib.SMTP_SSL(host, port)
            else:
                self.smtp_client = smtplib.SMTP(host, port)
            self.smtp_client.login(
                self.config.username.get_value(), self.config.password.get_value()
            )
        return self.smtp_client

    def send(self, receivers, text, title, body_type="html"):
        client = self.connect_smtp()
        msg_obj = MIMEMultipart()
        msg_obj["subject"] = title
        msg_obj["from"] = self.config.sender.get_value()
        msg_obj["to"] = ",".join(receivers)
        txt = MIMEText(text, body_type, "utf-8")
        msg_obj.attach(txt)
        return client.sendmail(
            self.config.sender.get_value(), receivers, msg_obj.as_string()
        )

    def send_html(self, path):
        self.send(open(path, "r").read(), "html")

    # --- IMAP ---

    def connect_imap(self):
        if self.imap_client is None:
            host = self.config.imap_host.get_value()
            port = int(self.config.imap_port.get_value())
            use_ssl = self.config.use_ssl.get_value() == "1"
            if use_ssl:
                self.imap_client = imaplib.IMAP4_SSL(host, port)
            else:
                self.imap_client = imaplib.IMAP4(host, port)
            self.imap_client.login(
                self.config.username.get_value(), self.config.password.get_value()
            )
        return self.imap_client

    def list_folders(self):
        client = self.connect_imap()
        result, data = client.list()
        if result != "OK":
            raise Exception(f"Failed to list folders: {data}")
        folders = []
        for item in data:
            item_str = item.decode("utf-8", errors="replace")
            parts = item_str.split(' "/" ')
            if len(parts) == 2:
                folder = parts[1].strip().strip('"')
                folders.append(folder)
        return folders

    def _decode_folder(self, folder):
        return folder.encode("utf-7").decode("utf-8") if isinstance(folder, str) else folder

    def list_emails(self, folder="INBOX", page=1, page_size=20, search_criteria="ALL"):
        client = self.connect_imap()
        folder_encoded = self._decode_folder(folder)
        result, _ = client.select(folder_encoded)
        if result != "OK":
            raise Exception(f"Failed to select folder: {folder}")

        result, data = client.search(None, search_criteria)
        if result != "OK":
            raise Exception(f"Search failed: {data}")

        msg_ids = data[0].split() if data[0] else []
        total = len(msg_ids)
        start = (page - 1) * page_size
        end = start + page_size
        page_ids = msg_ids[start:end] if msg_ids else []

        emails = []
        for msg_id in page_ids:
            result, msg_data = client.fetch(msg_id, "(FLAGS BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
            if result != "OK":
                continue
            raw_email = msg_data[0][1] if len(msg_data[0]) > 1 else b""
            if not raw_email:
                continue
            msg = email.message_from_bytes(raw_email)
            emails.append({
                "id": msg_id.decode(),
                "from": _decode_email_header(msg.get("From", "")),
                "subject": _decode_email_header(msg.get("Subject", "")),
                "date": str(msg.get("Date", "")),
                "flags": [f.decode() for f in msg_data[0][0].split()[1:]] if msg_data[0][0] else [],
            })
        client.close()
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "emails": emails,
        }

    def get_email(self, msg_id, folder="INBOX"):
        client = self.connect_imap()
        folder_encoded = self._decode_folder(folder)
        result, _ = client.select(folder_encoded)
        if result != "OK":
            raise Exception(f"Failed to select folder: {folder}")

        result, msg_data = client.fetch(msg_id, "(FLAGS BODY[])")
        if result != "OK":
            raise Exception(f"Failed to fetch email {msg_id}: {msg_data}")

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        body, html = _get_email_body(msg)
        attachments = _get_attachments(msg)

        result = Node(
            value={
                "id": msg_id,
                "from": _decode_email_header(msg.get("From", "")),
                "to": _decode_email_header(msg.get("To", "")),
                "cc": _decode_email_header(msg.get("Cc", "")),
                "subject": _decode_email_header(msg.get("Subject", "")),
                "date": str(msg.get("Date", "")),
                "body": body,
                "html": html,
                "attachments": attachments,
                "flags": [f.decode() for f in msg_data[0][0].split()[1:]] if msg_data[0][0] else [],
            }
        )
        client.close()
        return result

    def delete_emails(self, msg_ids, folder="INBOX"):
        client = self.connect_imap()
        folder_encoded = self._decode_folder(folder)
        result, _ = client.select(folder_encoded)
        if result != "OK":
            raise Exception(f"Failed to select folder: {folder}")
        for msg_id in msg_ids:
            client.store(msg_id, "+FLAGS", "\\Deleted")
        client.expunge()
        client.close()
        return Node(value=True)

    def move_emails(self, msg_ids, target_folder, source_folder="INBOX"):
        client = self.connect_imap()
        src_encoded = self._decode_folder(source_folder)
        dst_encoded = self._decode_folder(target_folder)
        result, _ = client.select(src_encoded)
        if result != "OK":
            raise Exception(f"Failed to select folder: {source_folder}")
        for msg_id in msg_ids:
            client.copy(msg_id, dst_encoded)
            client.store(msg_id, "+FLAGS", "\\Deleted")
        client.expunge()
        client.close()
        return Node(value=True)

    def mark_seen(self, msg_ids, folder="INBOX"):
        client = self.connect_imap()
        folder_encoded = self._decode_folder(folder)
        result, _ = client.select(folder_encoded)
        if result != "OK":
            raise Exception(f"Failed to select folder: {folder}")
        for msg_id in msg_ids:
            client.store(msg_id, "+FLAGS", "\\Seen")
        client.close()
        return Node(value=True)

    def mark_unseen(self, msg_ids, folder="INBOX"):
        client = self.connect_imap()
        folder_encoded = self._decode_folder(folder)
        result, _ = client.select(folder_encoded)
        if result != "OK":
            raise Exception(f"Failed to select folder: {folder}")
        for msg_id in msg_ids:
            client.store(msg_id, "-FLAGS", "\\Seen")
        client.close()
        return Node(value=True)

    def close_smtp(self):
        if self.smtp_client:
            try:
                self.smtp_client.quit()
            except Exception:
                pass
            self.smtp_client = None

    def close_imap(self):
        if self.imap_client:
            try:
                self.imap_client.logout()
            except Exception:
                pass
            self.imap_client = None

    def close(self):
        self.close_smtp()
        self.close_imap()


if __name__ == "__main__":
    f = File("data/email.json").write_if_not_exists(dict(sender=[], env_name=""))
    logger.info(f)
    conf = f.read_file()
    EmailUtil(conf["env_name"]).send(conf["sender"], "text", "title")
