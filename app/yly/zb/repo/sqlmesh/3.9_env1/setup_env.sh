pip install -e examples/custom_materializations
echo '__version__ = "0.0.0"' > sqlmesh/_version.py
pip install 'PyGithub>=2.6.0'
pip install "google-auth"
pip install "google-cloud-bigquery"
pip install "google-cloud-bigquery-storage"