import sys
from common.util.log import log
class TestBase:
    def __init__(self) -> None:
        pass

    def run(self):
        getattr(self,'test_'+sys.argv[1])()

    def expect(self,a,b,info=""):
        if a==b or str(a)==str(b):
            return True
        raise Exception(f'{a}!={b} [{info}]')
        