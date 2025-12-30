pip install -e .
pip install -e examples/custom_materializations
pip install agate
pip install "pyspark~=3.5.0"
pip install google-cloud-bigquery[pandas]
pip install time_machine
echo '__version__ = "0.0.0"' > sqlmesh/_version.py