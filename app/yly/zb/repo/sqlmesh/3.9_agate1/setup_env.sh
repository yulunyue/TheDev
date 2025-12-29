pip install -e .[bigquery]
pip install agate==1.7.1
pip install snowflake-connector-python[pandas,secure-local-storage]
pip install dbt-core
pip install dbt-duckdb>=1.7.1
echo '__version__ = "0.0.0"' > sqlmesh/_version.py