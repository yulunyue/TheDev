pip install -e .
pip install agate
pip install --force-reinstall "sqlglot==10.6.4"
pip install pydantic==1.10.13
pip install PyGithub
pip install google-auth
pip install tenacity
pip install "apache-airflow==2.3.3"
pip install --force-reinstall "pendulum==1.4.1"
echo '__version__ = "0.0.0"' > sqlmesh/_version.py