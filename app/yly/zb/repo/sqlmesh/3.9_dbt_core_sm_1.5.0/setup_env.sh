pip install -e .[bigquery]
pip install freezegun
pip install "dbt-core==0.19.1"
pip install "dbt-bigquery"
echo '__version__ = "0.0.0"' > sqlmesh/_version.py