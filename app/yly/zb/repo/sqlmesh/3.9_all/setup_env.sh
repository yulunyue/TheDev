pip install -e .[bigquery,redshift,postgres,athena,trino]
pip install -e examples/custom_materializations
pip install agate==1.7.1
pip install dbt-core
pip install dbt-duckdb>=1.7.1
echo '__version__ = "0.0.0"' > sqlmesh/_version.py
