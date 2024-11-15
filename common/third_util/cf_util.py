import os
from codeforces import problem
os.environ.setdefault("http_proxy", "http://proxy.huawei.com:8080")
os.environ.setdefault("https_proxy", "http://proxy.huawei.com:8080")
print(problem.get_info(175, "E"))
print("a")
