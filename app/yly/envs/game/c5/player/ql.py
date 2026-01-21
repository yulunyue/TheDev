from common.algo.export import Qlearning, State
from common.util.export import logger


class Ql(Qlearning):
    train_epoll_update = 1

    def train_before(self):
        self.get_model_file(f"view").remove()
        return super().train_before()

    def train_update_model(self, i, state: State):
        logger.info(
            self.get_model_file(f"view/{i}.log").write_file(state.show(algo=self))
        )
