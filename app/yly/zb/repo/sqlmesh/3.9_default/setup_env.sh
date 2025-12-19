cd /testbed/TobikoData/sqlmesh
git reset --hard ab6bc178cf4317388e560730ae27004af07645de
conda create -n testbed -y python=3.9
conda run -n testbed python -m venv /.venv/sqlmesh/posix_3.9_default
pip install --upgrade pip
pip install -e .
pip install pytest pytest-json-report toml debugpy pytest_mock pytest-xdist