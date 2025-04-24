import sys
from common.export import run, MainHander, install, check, PORT, manage
from app.yly.export import gm
from app.tool.export import api, file

GS = [manage, file, api]
if __name__ == "__main__":
    if sys.argv[1] == "install":
        install()
    elif sys.argv[1] == "check":
        check()
    elif sys.argv[1] == "run":
        run(GS, port=PORT)
