pip install -e .[bigquery,redshift,dlt]
pip install -e examples/custom_materializations
echo '__version__ = "0.0.0"' > sqlmesh/_version.py
