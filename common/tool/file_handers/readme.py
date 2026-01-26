from typing import List
from common.util.fp import File
from common.util.log import logger
import os


class ReadmeField:
    def __init__(self) -> None:
        self.init()
    
    def init(self):
        pass
    
    def set_title(self,title,level=1):
        self.title=title
        self.level=level
        return self

    def set_data(self,data):
        return self

    def lines(self):
        return []



class ReadmeLine(ReadmeField):
    
    def lines(self):
        return [f'{"#"*self.level} {self.title}']


class ReadmeImg(ReadmeField):
    pass

class ReadmeGraph(ReadmeField):
    def set_data(self, data):
        self.titles=[]
        self.graph_line=[]
        if not data['childs']:
            self.graph_line.append(data['title']+";")
            return self
        def dfs(node):
            if node["value"]:
                self.titles.append(f'### {node["value"]}')
            for cd in node['childs']:
                self.graph_line.append(f'{node["title"]}-->{cd["title"]};')
                dfs(cd)
        # logger.info(data)
        dfs(data)      
        return self  
    def lines(self):
        ret = self.titles+['```mermaid','graph']+self.graph_line
        ret.append('```')
        return ret 

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
            ret.append(f'|{i}|'+'|'.join([str(r.get(c,'')) for c in self.columns])+'|')
        ret.append('# ')
        return ret
            

class ReadmeGen:
    def __init__(self, path) -> None:
        self.fields: List[ReadmeField] = []
        self.store_dir=File(path)
        self.save_file=File(path+'.md')
        self.fields.append(ReadmeLine().set_title(f'LunYue ---Md Debug---'))
    
    def add_filed(self):
        pass

    def save(self):
        lines = []
        for fd in self.fields:
            lines += fd.lines()
        self.save_file.write_file("\n".join(lines))

    def add_table(self,data:dict):
        table=ReadmeTable()
        for k in data:
            table.add_column(k)
        table.add_row(data)
        self.fields.append(table)
        return self
    
    def set_frames(self,datas):
        table=ReadmeTable()
        for i in range(len(datas)):
            data=dict()
            gp=[]
            for k,v in datas[i].items():
                if v['type']=='graph':
                    gp.append(ReadmeGraph().set_title(
                        f'{k}:{i}').set_data(v))
                    continue
                table.add_column(k)
                data[k]=v['title']
            if data:
                table.rows.append(data)
            if gp:
                if table.rows:
                    self.fields.append(table)
                    table=ReadmeTable()
                self.fields.extend(gp)
                gp.clear()
        if table.rows:
            self.fields.append(table)
        return self