from common.service.http import run, MainHander
from app.yly.algo import manage
from common.tool.ts_file import TsFile
TS_MOCK_PATH = 'font/src/model/mock.ts'
if __name__ == '__main__':
    MainHander.POST_API.add_hock(TsFile().load(TS_MOCK_PATH).update_api)
    run(manage)
