pip install -e .
pip install google-cloud-bigquery
pip install google-cloud-bigquery-storage
pip install -e examples/custom_materializations
pip install redshift_connector
pip install PyAthena[Pandas]
#pip install psycopg2
pip install trino
pip install "agate==1.7.1"
pip install dbt-core
pip install "dbt-duckdb>=1.7.1"
pip install snowflake-connector-python[pandas,secure-local-storage]
echo '__version__ = "0.0.0"' > sqlmesh/_version.py
