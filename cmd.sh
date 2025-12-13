python -m cpp.pytool.main execute path=cpp/src/loj_p2885.cpp
python -m tests.test_algo
python -m app.yly.main lc_757.py test
python -m tests.test_tf

python -m tool.pytes dev 
python -m tool.dfx app.yly.envs.cg.cw.main.Solution dev execute
python -m tool.docker_cli build app/yly/zb/CTFd__CTFd-1922/Dockerfile


python -m app.yly.zb.main 6652 main
python -m app.yly.zb.manage main key=briefcase
python -m app.yly.zb.manage web_run
python .\verify.py task/briefcase/beeware_6035_briefcase-1058
docker rm zb
docker run -v d:/thebug/TheDev:/d:/thebugTheDev --name zb -it zb:latest
docker exec -it zb /bin/bash

pytest tests/console/test_Log.py::test_save_log_to_file_fail_to_write_file
rm -rf briefcase
ln -s /TheDev/data/repo/beeware/briefcase briefcase
mklink 


python -m app.yly.zb.main 6040 patch_repair path=tests/platforms/macOS/app/test_signing.py