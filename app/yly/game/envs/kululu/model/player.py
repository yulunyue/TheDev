class Player:
    EXPLORER = "EXPLORER"
    WANDERER = "WANDERER"

    def __init__(self, entity_type, key, x, y, param_0, param_1, param_2) -> None:
        self.x = int(x)
        self.y = int(y)
        self.entity_type = entity_type
        self.key = key
