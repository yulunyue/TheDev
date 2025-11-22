python -m pip install --upgrade pip
python -m pip install pytest-json-report
cd data/repo/vllm-project/vllm
python -m pip install -r requirements-dev.txt
python -m pip install -r requirements-common.txt
python -m pip install transformers==4.48.3