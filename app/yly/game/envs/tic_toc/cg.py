from common.mock import CgMock


class TicTocCg(CgMock):
    def run(self):
        while True:
            opponent_row, opponent_col = [int(i) for i in self.input().split()]
            valid_action_count = int(self.input())
            for i in range(valid_action_count):
                row, col = [int(j) for j in self.input().split()]
            if opponent_row != -1 and opponent_col == -1:
                self.mv = self.do(opponent_row, opponent_col)
            if self.mv:
                self.search.search(self.mv)
                self.mv = self.mv.best_action
            else:
                self.mv = Move(4, 4, self.op)
            self.do(self.mv.y, self.mv.x)
            y1, x1, y2, x2 = (
                self.mv.y // 3,
                self.mv.y % 3,
                self.mv.x // 3,
                self.mv.x % 3,
            )
            return f"{y1*3+y2} {x1*3+x2}"


if __name__ == "__main__":
    TicTocCg().run()
