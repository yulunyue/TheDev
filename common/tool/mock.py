class Mock:
    def __init__(self,name):
        self.name=name
    def __getattribute__(self,name):
        return self
    def __call__(self,*args,**kw):
        return self
