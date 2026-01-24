from common.tool.export import Mock
try:
    import numpy as np
    np.set_printoptions(suppress=True, precision=4)
except Exception as e:
    np=Mock("np")


