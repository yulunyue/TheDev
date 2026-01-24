from common.third_util.ml.tf_util import TfModule, keras, np
from .constant import C

TODOTODOTODOT = 1


class OaTfModule(TfModule):
    def __init__(self):
        inputs = keras.Input(shape=(C.INPUT_SIZE,), name="input")
        # Common part of the Model, both policy and value use these layers
        x = keras.layers.Dense(TODOTODOTODOT, activation="relu", name="Dense1")(inputs)
        # x = tf.keras.layers.Dense(TODOTODOTODOT,activation='relu')(x)

        # Split part 1, P1 layers are for the policy part. If you don't want extra layers for p1, I guess you can do p1=x
        p1 = keras.layers.Dense(TODOTODOTODOT, activation="relu", name="p1")(x)
        # p1 = tf.keras.layers.Dense(TODOTODOTODOT,activation='relu')(p1)

        # Split part, v1 layers are for the value part. If you don't want extra layers for v1, I guess you can do v1=x
        v1 = keras.layers.Dense(TODOTODOTODOT, activation="relu", name="v1")(x)
        # v1 = tf.keras.layers.Dense(TODOTODOTODOT,activation='relu')(v1)
        # Output layers, don't touch them if you don't know what are you doing.
        value = keras.layers.Dense(1, activation="tanh", name="value")(v1)
        policy = keras.layers.Dense(C.POLICY_SIZE, activation="softmax", name="policy")(
            p1
        )
        self.model = keras.Model(inputs=inputs, outputs=[value, policy])
        # Others use Adam as optimizer, I just used SGD because I'm clueless and I saw some others using SGD.
        opt = keras.optimizers.SGD(
            learning_rate=C.K_LEARNING_RATE, momentum=C.K_MOMENTUM
        )
        # Keep a file with losses history
        SAMPLES_FILE = "D:/thebug/CGZero/traindata/samples.dat"
        csv_data: np.ndarray = np.fromfile(SAMPLES_FILE, dtype=np.float32).reshape(
            (-1, C.INPUT_SIZE + C.POLICY_SIZE + 2)
        )

        cut_index = [
            (csv_data.shape)[1] - C.POLICY_SIZE - 2,
            (csv_data.shape)[1] - 2,
            (csv_data.shape)[1] - 1,
        ]
        csv_logger = keras.callbacks.CSVLogger("data/log/gen_train.log", append=True)
        samples, policy, value, countVisits = np.split(csv_data, cut_index, axis=1)
        self.model.compile(
            loss={"value": "mean_squared_error", "policy": keras.losses.KLD},
            optimizer=opt,
            loss_weights={"value": 1.0, "policy": 1.0},
            metrics={
                "value": "mean_absolute_percentage_error",
                "policy": "categorical_accuracy",
            },
        )
        generation = 0
        self.model.fit(
            {"input": samples},
            {"policy": policy, "value": value},
            verbose=2,
            epochs=min(generation + 1, 40),
            callbacks=[csv_logger],
            batch_size=64,
        )
