from .env import PenduState, QNet
from common.util.export import ToolBase, logger
from .algo import DoubleDqn
from .constant import C


class ToolPen(ToolBase):

    def prepare(self, *args):
        self.s = PenduState()

    def run_dbdqn(self):

        dqn = (
            DoubleDqn()
            .load(
                train_epoll=200,
                gamma=0.98,
                e_greed=0.01,
                learning_rate=1e-2,
            )
            .set_model(QNet, target_update=50)
        )
        dqn.train(self.s)

    def dev(self):
        self.run_dbdqn()

    def debug(self):
        self.dev()


if __name__ == "__main__":
    ToolPen().run()
