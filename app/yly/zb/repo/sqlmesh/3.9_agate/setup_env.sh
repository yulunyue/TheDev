pip install -e examples/custom_materializations
pip install agate=1.7.1
pip install snowflake-connector-python[pandas,secure-local-storage]
pip install dbt-core
echo '__version__ = "0.0.0"' > sqlmesh/_version.py