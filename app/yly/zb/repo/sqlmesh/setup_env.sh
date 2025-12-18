cd /testbed/TobikoData/sqlmesh
git reset --hard bd768a9993866fdff2f9f8f827b437ad96a9f8a1
conda create -n testbed -y python=3.9
conda run -n activate testbed python -m venv {self.venv_dir}
/.venv/sqlmesh/posix_3.9/bin/python -m pip install --upgrade pip
/.venv/sqlmesh/posix_3.9/bin/python -m pip install -e .
pip install pytest pytest-json-report toml debugpy pytest_mock pytest-xdist