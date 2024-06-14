import matplotlib.pyplot as plt
class Draw:
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()
    
    def draw_bar_chart(self,lines):
        self.ax.bar(
            [l[0] for l in lines],
            [l[1] for l in lines]
        )
        return self

    def draw_graph(self,datas):
        import networkx as nx
        plt.figure(figsize=(8,8))
        g = nx.DiGraph()
        nodes=[]
        edges=dict()
        for f,t in datas:
            edges[(f,t)]=f'{f}_{t}'
            nodes.append((f,t))
        g.add_edges_from(nodes)
        pos = nx.layout.spring_layout(g,iterations=1, seed=227)
        nx.draw(
            g, pos, node_color='#aaa',node_shape='s',
            with_labels=True,node_size=800,
            alpha=1
        )
        nx.draw_networkx_edge_labels(
            g,pos,edge_labels=edges,font_color='#000'
        )
        return self

    def save(self, path):
        plt.savefig(path)
        return self

    def test(self):
        self.draw_bar_chart([
            [2,3],[4,5]
        ])
        self.save('data/test/test.png')

if __name__=='__main__':
    Draw().test()
