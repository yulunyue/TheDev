import time
import sys


def progress_bar(current, total, bar_length=50):
    percent = float(current) * 100 / total
    arrow = "-" * int(percent / 100 * bar_length - 1) + ">"
    spaces = " " * (bar_length - len(arrow))

    sys.stdout.write(f"\r进度: [{arrow}{spaces}] {percent:.2f}%")
    sys.stdout.flush()


# 使用示例
total = 100
for i in range(total):
    time.sleep(0.1)  # 模拟任务
    progress_bar(i + 1, total)
