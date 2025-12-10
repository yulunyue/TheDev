#!/bin/bash

# 遇到任何错误立即退出，确保脚本的健壮性
 
set -e

git clone https://github.com/python-poetry/poetry.git /testbed/poetry
cd /testbed/poetry
git checkout 0b38fada8dfc41bf6a47288781785373d663185e
rm -f poetry.lock
poetry lock
poetry install
# poetry env use 3.9
cd /