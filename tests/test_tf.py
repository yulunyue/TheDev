from common.util.export import TestBase, logger
from common.third_util.tf_util import tf, keras, print_cpu_info


class TestTf(TestBase):
    def dev(self):
        logger.map(kera=tf.keras.__file__)


if __name__ == "__main__":
    TestTf().run()
