class Study:
    def __init__(self) -> None:
        self.visite_count=0

    @property
    def a(self):
        self.visite_count+=1
        return self.visite_count
    
