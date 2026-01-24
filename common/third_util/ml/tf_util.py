import os

os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
import tensorflow as tf
from keras._tf_keras import keras


class TfModule:
    pass


def print_cpu_info():

    print("TF:" + tf.__version__)
    print(
        "GPU:"
        + str(tf.config.list_physical_devices("GPU"))
        + " CUDA:"
        + str(tf.test.is_built_with_cuda())
    )
