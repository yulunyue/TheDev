pip install -e .[bigquery]
pip install freezegun
pip install "dbt-core==0.19.1"
pip install "dbt-bigquery"
pip install "pydantic==1.10.13"
echo '__version__ = "0.0.0"' > sqlmesh/_version.py