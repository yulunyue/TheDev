from common.util.export import TestBase, logger


class TestTf(TestBase):
    def dev(self):
        from common.third_util.tf_util import tf, keras, print_cpu_info

        logger.map(kera=tf.keras.__file__)
        print_cpu_info()


if __name__ == "__main__":
    TestTf().run()
