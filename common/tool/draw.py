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
