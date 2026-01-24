pip install -e .
pip install -e examples/custom_materializations
pip install google-cloud-bigquery
pip install PyGithub
echo '__version__ = "0.0.0"' > sqlmesh/_version.py
echo '__version_tuple__ = (0,0,0)' >> sqlmesh/_version.py