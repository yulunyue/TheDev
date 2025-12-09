python -m cpp.pytool.main execute path=cpp/src/loj_p2885.cpp
python -m tests.test_algo
python -m app.yly.main lc_757.py test
python -m tests.test_tf
python -m app.yly.zb.main beeware__briefcase-1006 init
python -m tool.pytes dev 
python -m tool.dfx app.yly.envs.cg.cw.main.Solution dev execute

python -m tool.docker_cli build app/yly/zb/CTFd__CTFd-1922/Dockerfile