pip install -e .
pip install agate
pip install --force-reinstall "sqlglot==11.1.2"
pip install pydantic==1.10.13
pip install PyGithub
pip install google-auth
pip install tenacity
pip install pyarrow==11.0.0
pip install dbt-core
echo '__version__ = "0.0.0"' > sqlmesh/_version.py