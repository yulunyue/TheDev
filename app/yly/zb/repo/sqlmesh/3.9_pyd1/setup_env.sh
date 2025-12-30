pip install -e .[bigquery]
pip install freezegun
pip install "dbt-core<1.6.0"
pip install "dbt-bigquery"
pip install "pydantic==1.10.13"
echo '__version__ = "0.0.0"' > sqlmesh/_version.py