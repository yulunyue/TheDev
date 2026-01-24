pip install -e .[bigquery]
pip install --upgrade --force-reinstall pandas
pip install pyspark>=3.4.0
echo '__version__ = "0.0.0"' > sqlmesh/_version.py