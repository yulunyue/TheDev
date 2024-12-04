from typing import List
from common.util.fp import File
import os


class ReadmeField:
    def __init__(self) -> None:
        self.init()
    
    def init(self):
        pass

    def set_data(self,data):
        return self

    def lines(self):
        return []



class ReadmeLine(ReadmeField):
    def set_title(self,title,level=1):
        self.title=title
        self.level=level
        return self
    
    def lines(self):
        return [f'{"#"*self.level} {self.title}']


class ReadmeImg(ReadmeField):
    pass

class ReadmeTree(ReadmeField):
    pass

class ReadmeTable(ReadmeField):

    def init(self):
        self.columns = set()
        self.rows = []
        return self
    
    def add_column(self,key):
        self.columns.add(key) 
        return self


    def add_row(self,rows):
        self.rows.append(rows)
        return self

    
    def lines(self):
        ret=['|-|'+'|'.join(self.columns)+'|']
        ret.append('|'+'|'.join(["---"]*(len(self.columns)+1))+'|')
        for i,r in enumerate(self.rows):
            ret.append(f'|{i}|'+'|'.join([r.get(c,'') for c in self.columns])+'|')
        return ret
            

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
        self.fields.append(ReadmeLine().set_title(f'LunYue ---Md Debug---'))
        table=ReadmeTable()
        for i in range(len(datas)):
            data=dict()
            for k,v in datas[i].items():
                if v['type']=='tree':
                    #self.fields.append(ReadmeTree().set_data(v))
                    continue
                table.add_column(k)
                data[k]=v['title']
            if data:
                table.rows.append(data)
        if table.rows:
            self.fields.append(table)
        return self