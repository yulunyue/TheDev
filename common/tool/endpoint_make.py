from typing import List
class EndPointMake:
    def __init__(self) -> None:
        self.endpoints:List[str]=[]
        self.keys=dict()
    def load(self, keys, endpoints):
        self.keys=keys
        self.endpoints=endpoints
        return self
    
    def load_from_json_file(self):
        pass
    
    def make(self):
        self.map_keys=[]
        ret=[]
        for endpoint in self.endpoints:
            key_map=self.get_line_key(endpoint)
            if not key_map:
                ret.append(endpoint)
                continue 
            ret+=self.render(endpoint,key_map)
        return ret
   
    def render(self,endpoint:str,keys):
        ret=[]
        m=dict()
        def dfs(i):
            if i>=len(keys):
                ret.append(endpoint.format(**m))
                return 
            for v in self.keys.get(keys[i],['']):
                m[keys[i]]=v
                dfs(i+1)
        dfs(0)
        return ret
    
    def get_line_key(self, key:str):
        ret=[]
        k=None
        for v in key:
            if v=='{':
                k=""
            elif v=='}' and k is not None:
                ret.append(k)
                k=None
            elif k is not None:
                k+=v
        return list(set(ret))

if __name__ == "__main__":
    print(EndPointMake().load(
        dict(
            a=['12','34'],
            b=['c']
        ),
        [
            "d{a}.{b}",
            "{a}.x{b}",
            "c{c}.{a}.x{b}",
        ]
    ).make())