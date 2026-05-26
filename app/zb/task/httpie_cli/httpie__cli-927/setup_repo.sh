set -e 

cd /testbed/cli
git checkout 492687b0dafb7bec0d6281d019bb5f4f60439346
source /opt/miniconda3/etc/profile.d/conda.sh
conda activate testbed

uv pip install "urllib3==1.26.6" "setuptools<59" -r requirements-dev.txt
uv pip install "urllib3==1.26.6" "setuptools<59" -e .[dev,test]
