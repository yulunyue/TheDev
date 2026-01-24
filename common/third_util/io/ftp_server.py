from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging
import os
from datetime import datetime
import sys


class CustomFTPHandler(FTPHandler):
    def on_connect(self):
        print(f"{datetime.now()} - 客户端连接: {self.remote_ip}:{self.remote_port}")

    def on_disconnect(self):
        print(f"{datetime.now()} - 客户端断开: {self.remote_ip}")

    def on_login(self, username):
        print(f"{datetime.now()} - 用户登录: {username} from {self.remote_ip}")

    def on_logout(self, username):
        print(f"{datetime.now()} - 用户登出: {username}")

    def on_file_sent(self, file):
        print(f"{datetime.now()} - 文件已发送: {file}")

    def on_file_received(self, file):
        print(f"{datetime.now()} - 文件已接收: {file}")

    def on_incomplete_file_sent(self, file):
        print(f"{datetime.now()} - 文件发送中断: {file}")

    def on_incomplete_file_received(self, file):
        print(f"{datetime.now()} - 文件接收中断: {file}")


def setup_ftp_server():
    # 设置日志
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

    # 创建授权管理器
    authorizer = DummyAuthorizer()

    # 创建用户目录
    user_dir = sys.argv[1]

    # 添加多个用户
    users = [
        {
            "name": sys.argv[2],
            "password": sys.argv[3],
            "perm": "elradfmwMT",
            "dir": user_dir,
        }
    ]

    for user in users:
        authorizer.add_user(
            user["name"], user["password"], user["dir"], perm=user["perm"]
        )

    # 添加匿名用户
    # authorizer.add_anonymous(f"{user_dir}/anonymous", perm="elr")

    # 配置处理器
    handler = CustomFTPHandler
    handler.authorizer = authorizer
    handler.banner = "欢迎使用Python FTP服务器"

    # 设置被动端口范围
    handler.passive_ports = range(60000, 60100)

    # 限制传输速率（字节/秒）
    handler.masquerade_address = None  # 设置为外部IP地址（如果使用NAT）
    handler.max_login_attempts = 3
    handler.timeout = 300  # 超时时间（秒）

    # 创建服务器
    address = ("0.0.0.0", int(sys.argv[4]))  # 标准FTP端口
    server = FTPServer(address, handler)

    # 服务器配置
    server.max_cons = 100
    server.max_cons_per_ip = 10

    return server


def main():
    print("=" * 50)
    print("Python FTP 服务器")
    print("=" * 50)
    print("用户列表:")
    print("=" * 50)

    server = setup_ftp_server()

    try:
        print("服务器正在启动...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器正在关闭...")
        server.close_all()
    except Exception as e:
        print(f"服务器错误: {e}")


if __name__ == "__main__":
    # 注意：在Linux/Mac上需要root权限才能使用21端口
    # 可以使用 sudo python ftp_server.py 或以非特权端口运行
    main()
