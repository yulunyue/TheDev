
from typing import List
import json


class BaseModel:
    def __init__(self, value, data_source=None) -> None:
        self.value = value
        self.data_source = data_source
        if self.data_source:
            self.data_source.add_param(self)
        self.ops=[]
        self.key = ""
        self.info=""
    def set_info(self,info):
        self.info=info
        return self
    
    def get_value(self) -> str:
        if self.data_source and self.key:
            ret = self.data_source.get_key_value(self.key)
            if ret is not None:
                self.value = ret
        return self.value

    def set_value(self, value):
        self.data_source.set_key_value(self.key, value)
        return self
    
    def __gt__(self,value):
        if isinstance(value,BaseModel):
            value=value.get_value()
        return self.get_value()<value

    def __sub__(self,value):
        if isinstance(value,BaseModel):
            value=value.get_value()
        self.value = self.value-value
        return self
    
    def __rsub__(self,value):
        if isinstance(value,BaseModel):
            value=value.get_value()
        self.value=value-self.value
        return self
    
    def __add__(self,value):
        if isinstance(value,BaseModel):
            value=value.get_value()
        self.value+=value
        return self
    
    def __radd__(self,value):
        return self.__add__(value)

    def __str__(self) -> str:
        return f'value:{self.value},{self.ops},{self.info}'

class StrModel(BaseModel):
    def __init__(self, data_source, value="") -> None:
        super().__init__(data_source, value)


class NumberModel(BaseModel):
    pass

def number(v):
    if isinstance(v,NumberModel):
        return v
    return NumberModel(v)

class DictModel(BaseModel):
    def __init__(self, data_source, value=None) -> None:
        super().__init__(data_source, value or dict())

    def get(self, key, default_value=None) -> dict:
        if key in self.value:
            return self.value[key]
        self.value[key] = default_value
        return default_value

    def get_value(self) -> dict:
        return super().get_value()


ENABLE = "enable"
DISABLE = "disable"


class EnableModel(BaseModel):
    def __init__(self, value=DISABLE) -> None:
        super().__init__(value)

    def get_value(self):
        return super().get_value() == ENABLE


class EncroyModel(BaseModel):
    def get_value(self) -> str:
        return json.load(open('data/doc/password.json', 'r'))[self.value]
    

if __name__=="__main__":
    print(number(3)+4-2)
