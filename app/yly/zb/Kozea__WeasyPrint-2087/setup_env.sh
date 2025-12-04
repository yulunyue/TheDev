python -m pip install --upgrade pip
cd data/repo/Kozea/WeasyPrint
python -m pip install pytest pytest-json-report toml
python -m pip install "pydyf>=0.8.0"
python -m pip install "cffi>=0.6"
python -m pip install "html5lib>=1.1"
python -m pip install "tinycss2>=1.0.0"
python -m pip install "cssselect2>=0.1"
python -m pip install "Pyphen>=0.9.1"
python -m pip install "Pillow>=9.1.0"
python -m pip install "fonttools[woff]>=4.0.0"
apt -y install libpango-1.0-0 libpangoft2-1.0-0 ghostscript