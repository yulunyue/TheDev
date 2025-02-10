class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.keys=[]
        self.store=dict()
    def get(self, key: int) -> int:
        if key in self.store:
            self.move_head(key)
            return self.store[key]
        return -1

    def put(self, key: int, value: int) -> None:
        self.store[key]=value  
        self.move_head(key)
    
    def move_head(self,key):
        if len(self.keys)<self.capacity:
            self.keys.insert(0,key)
            return
        idx=None
        for i,v in enumerate(self.keys):
            if v==key:
                idx=i
                break
        if idx is None:
            self.keys.insert(0,self.keys.pop(idx))
        else:
            s=self.keys.pop()
            self.keys.insert(0,s)
            self.store.pop(s)


