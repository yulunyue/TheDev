class Env:
    def __init__(self):
        self.actions=[]
        self.size=0
        self.state=0
        self.reward=0
    def reset(self):
        return self

    def get_actions(self):
        return self.actions

    def do(self,action):
        pass