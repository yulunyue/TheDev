set -e
mkdir -p /testbed/beeware
git config --global http.sslVerify false
git clone https://github.com/beeware/briefcase.git /testbed/beeware/briefcase
conda create -n testbed -y