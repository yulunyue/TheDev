import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.parser import Parser
import json
import poplib

from common.tool.export import FileConfig, StrModel
from common.util.export import File, logger


class EmailConfig(FileConfig):
    username = StrModel()
    password = StrModel()
    hostname = StrModel()
    sender = StrModel()


EmailConfig.set_resource("config/setting/email.json")


class EmailUtil:
    def __init__(self, env_name) -> None:
        self.client: smtplib.SMTP = None
        self.recv_client: poplib.POP3 = None
        self.env_name = env_name
        self.config = EmailConfig.get(env_name)

    def connect(self):
        if self.client is None:
            self.client = smtplib.SMTP()
            assert self.config.hostname.get_value()
            self.client.connect(self.config.hostname.get_value())
            self.client.login(
                self.config.username.get_value(), self.config.password.get_value()
            )
        return self.client

    def send(self, receivers, text, title):
        client = self.connect()
        msg_obj = MIMEMultipart()
        msg_obj["subject"] = title
        msg_obj["from"], msg_obj["to"] = self.config.sender.get_value(), ",".join(
            receivers
        )
        txt = MIMEText(text, "html", "utf-8")
        msg_obj.attach(txt)
        return client.sendmail(
            self.config.sender.get_value(), receivers, msg_obj.as_string()
        )

    def send_html(self, path):
        self.send(open(path, "r").read(), "html")

    def close(self):
        self.client.quit()


if __name__ == "__main__":
    f = File("data/email.json").write_if_not_exists(dict(sender=[], env_name=""))
    logger.info(f)
    conf = f.read_file()
    EmailUtil(conf["env_name"]).send(conf["sender"], "text", "title")
