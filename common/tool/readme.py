from typing import List
from common.util.fp import File
import os


class ReadmeField:
    def __init__(self) -> None:
        pass

    def lines(self):
        return []

    def set_info(self, **kw):
        return self

class ReadmeLine(ReadmeField):
    def set_title(self,title):
        self.title=title
        return self
    
    def set_info(self, key, title,**kw):
        self.title = f'{key} {title}'
        return self
    
    def lines(self):
        return [f'## {self.title}']

class ReadmeImg(ReadmeField):
    pass

class ReadmeTable(ReadmeField):
    pass

class ReadmeGen:
    def __init__(self, path) -> None:
        self.fields: List[ReadmeField] = []
        self.store_dir=File(path)
        self.save_file=File(path+'.md')
    
    def add_filed(self):
        pass

    def save(self):
        lines = []
        for fd in self.fields:
            lines += fd.lines()
        self.save_file.write_file("\n".join(lines))

    def set_frames(self,datas):
        self.fields = []
        for i in range(len(datas)):
            self.fields.append(ReadmeLine().set_title(f'frame {i}'))
            for k,v in datas[i].items():
                self.fields.append(ReadmeLine().set_info(**v))
        return self