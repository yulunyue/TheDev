from common.algo.export import Sarse
from common.util.export import File, logger
from ..constant import C


class SarseCf(Sarse):
    def load(self, n_step=1, **kw):
        return super().load(n_step, **kw).set_train_epoll(1000)

    def view(self):
        return C.view(self)

    def train_one(self, i, state):
        ret = super().train_one(i, state)
        # f = File(f"data/algo/{self.get_name()}/{i}.json")
        # logger.info(f.write_file(self.q))
        return ret
