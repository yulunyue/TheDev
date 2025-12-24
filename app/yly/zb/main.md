cd /testbed/beeware/briefcase
git reset --hard ef8e8f9069e9e26ba77ce5d2639503a341413a4d
conda run -n testbed python --version
conda run -n testbed python -c 'import sys;print(sys.executable)'
conda run -n testbed python -m pip config set global.index-url https://pypi.cloudartifact.dgg.dragon.tools.huawei.com/artifactory/api/pypi/cbu-pypi-public/simple/
conda run -n testbed python -m pip config set global.trusted-host pypi.cloudartifact.dgg.dragon.tools.huawei.com
conda run -n testbed python -m pip config get global.index-url
conda run -n testbed python -m pip config get global.trusted-host
conda run -n testbed python -m pip install --upgrade pip
conda run -n testbed python -m pip install -e .
conda run -n testbed python -m pip install pytest pytest-json-report toml debugpy pytest_mock pytest-xdist