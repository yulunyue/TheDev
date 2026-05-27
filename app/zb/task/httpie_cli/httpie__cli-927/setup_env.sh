set -e

conda create -n testbed python=3.8 -y
source /opt/miniconda3/etc/profile.d/conda.sh
conda activate testbed

pip install uv
git clone https://github.com/httpie/cli.git /testbed/cli
