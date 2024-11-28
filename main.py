import sys
from common.service.http import run, MainHander
from common.tool.cid import install,check,PORT
from app.yly.game import gm
from app.yly.algo import manage
GS=[gm,manage]
if __name__ == '__main__':
    if sys.argv[1]=='install':
        install()
    elif sys.argv[1]=='check':
        check()
    elif sys.argv[1]=='run':
        run(*GS,port=PORT)

