class Constant:
    EXPLORER = "EXPLORER"
    WANDERER = "WANDERER"
    TYPE_WALL = "#"
    TYPE_NULL = "."
    TYPE_SPAWN_FOR_WANDERER = "w"
    ACTION_WAIT = "WAIT"
    ACTION_MOVE = "MOVE"
    DR = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    def get_cases(self):
        pass


C = Constant()
