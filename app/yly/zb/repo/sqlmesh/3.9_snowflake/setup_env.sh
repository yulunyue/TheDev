pip install -e .
pip install snowflake-connector-python
pip install snowflake-snowpark-python
pip install -e examples/custom_materializations
echo '__version__ = "0.0.0"' > sqlmesh/_version.py