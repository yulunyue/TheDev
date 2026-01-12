# setup.py
from setuptools import setup, find_packages
import os


setup(
    name="the_dev",
    version="0.1.0",
    package_dir={
        "common": "common",
    },
    packages=["common"],
    # 其他配置...
)
