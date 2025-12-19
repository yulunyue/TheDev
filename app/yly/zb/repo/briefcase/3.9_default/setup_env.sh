cd /testbed/beeware/briefcase
git reset --hard 29f6745a6f2eb632a8ab4f739c652bcbbcdc4bfe
conda create -n testbed -y python=3.9
conda run -n testbed python -m venv /.venv/briefcase/posix_3.9_default
pip install --upgrade pip
pip install -e .
pip install pytest pytest-json-report toml debugpy pytest_mock pytest-xdist
pip install "coverage[toml] == 7.4.4"
pip install "coverage-conditional-plugin == 0.9.0"
pip install "pre-commit == 3.5.0 ; python_version < '3.9'"
pip install "pre-commit == 3.7.0 ; python_version >= '3.9'"
pip install "pytest == 8.1.1"
pip install "pytest-xdist == 3.5.0"
pip install "setuptools_scm == 8.0.4"
pip install "tox == 4.14.2"
pip install "httpx<1.0"
pip install "tomli_w"
pip install "truststore"
pip install "httpx_retries"