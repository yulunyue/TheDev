pip install -e .
pip install agate
pip install pydantic==1.10.13
pip install google-auth
pip install --force-reinstall "sqlglot==10.4.1"
pip install tenacity
pip install "apache-airflow==2.3.3"
echo '__version__ = "0.0.0"' > sqlmesh/_version.py