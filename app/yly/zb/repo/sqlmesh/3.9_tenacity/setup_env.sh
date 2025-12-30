pip install -e .[bigquery]
pip install freezegun
pip install "dbt-core<1.6.0"
pip install "tenacity==8.1.0"
pip install 'apache-airflow==2.3.3'
echo '__version__ = "0.0.0"' > sqlmesh/_version.py