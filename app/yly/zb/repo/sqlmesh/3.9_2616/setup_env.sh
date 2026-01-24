pip install -e .
pip install agate
pip install --force-reinstall "sqlglot[rs]~=23.17.0"
pip install pydantic==1.10.13
pip install PyGithub
pip install google-auth
pip install tenacity
pip install dbt-snowflake
pip install "apache-airflow==2.3.3"
echo '__version__ = "0.0.0"' > sqlmesh/_version.py