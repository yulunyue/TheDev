import sys
from common.export import run, MainHander, install, check, PORT, manage
from app.yly.export import gm
from app.tool.export import api, file
from app.test import TestTheDev

GS = [gm, manage, file, api]
if __name__ == "__main__":
    if sys.argv[1] == "install":
        install()
    elif sys.argv[1] == "check":
        check()
    elif sys.argv[1] == "run":
        MainHander.POST_API.load_modules(GS)
        run(port=PORT)
    elif sys.argv[1] == "test":
        MainHander.POST_API.load_modules(GS)
        TestTheDev().run(sys.argv[2:])
