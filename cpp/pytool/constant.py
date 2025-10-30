class Constant:
    GCC = "g++"
    O_FLAG = "-o"
    DEBUG_FLAG = "-g"
    CPP_SUFIX = ".cpp"
    C_SUFIX = ".c"
    BIN_SUFFIX = ".exe"
    LIB_SUFFIX = ".dll"
    OUT_PUT_DIR = "data/build/cpp"

    def I(self, name):
        return f"-I {name}"


C = Constant()
