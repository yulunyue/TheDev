import numpy as np
import random
from collections import defaultdict
import pickle
import os


class TicTacToe:
    """三子棋游戏环境"""

    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.winner = None
        self.game_over = False

    def reset(self):
        """重置游戏"""
        self.board = [" "] * 9
        self.current_player = "X"
        self.winner = None
        self.game_over = False
        return self.get_state()

    def get_state(self):
        """获取当前状态（字符串表示）"""
        return "".join(self.board)

    def get_valid_moves(self):
        """获取合法动作"""
        return [i for i, cell in enumerate(self.board) if cell == " "]

    def make_move(self, position):
        """执行动作"""
        if self.board[position] == " " and not self.game_over:
            self.board[position] = self.current_player

            # 检查游戏是否结束
            self.check_game_over()

            # 切换玩家
            if not self.game_over:
                self.current_player = "O" if self.current_player == "X" else "X"

            return True
        return False

    def check_game_over(self):
        """检查游戏是否结束"""
        winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # 行
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # 列
            [0, 4, 8],
            [2, 4, 6],  # 对角线
        ]

        for combo in winning_combinations:
            if (
                self.board[combo[0]]
                == self.board[combo[1]]
                == self.board[combo[2]]
                != " "
            ):
                self.winner = self.board[combo[0]]
                self.game_over = True
                return

        if " " not in self.board:
            self.game_over = True
            self.winner = None  # 平局

    def render(self):
        """显示棋盘"""
        print("-------------")
        for i in range(3):
            print(f"| {self.board[i*3]} | {self.board[i*3+1]} | {self.board[i*3+2]} |")
            print("-------------")
        print(f"当前玩家: {self.current_player}")


class QLearningAgent:
    """Q-learning智能体"""

    def __init__(self, player="X", alpha=0.1, gamma=0.9, epsilon=0.1):
        self.player = player
        self.alpha = alpha  # 学习率
        self.gamma = gamma  # 折扣因子
        self.epsilon = epsilon  # 探索率
        self.q_table = defaultdict(lambda: np.zeros(9))  # Q表
        self.states_visited = set()

    def get_action(self, state, valid_moves, training=True):
        """根据当前状态选择动作"""
        state_key = self.get_state_key(state)

        if training and random.random() < self.epsilon:
            # 探索：随机选择合法动作
            return random.choice(valid_moves)
        else:
            # 利用：选择Q值最大的动作
            q_values = self.q_table[state_key]
            # 只考虑合法动作
            valid_q_values = {move: q_values[move] for move in valid_moves}
            if not valid_q_values:
                return None

            # 如果有多个相同最大值的动作，随机选择一个
            max_q = max(valid_q_values.values())
            best_moves = [move for move, q in valid_q_values.items() if q == max_q]
            return random.choice(best_moves)

    def get_state_key(self, state):
        """获取状态的规范化表示（考虑对称性）"""
        # 将状态转换为3x3矩阵
        board = [state[i] for i in range(9)]

        # 获取所有对称状态
        symmetries = self.get_symmetries(board)

        # 选择最小的字符串表示作为键（规范化）
        return min(symmetries)

    def get_symmetries(self, board):
        """获取棋盘的所有对称状态"""
        # 转换为3x3矩阵
        matrix = [board[i : i + 3] for i in range(0, 9, 3)]

        symmetries = []

        # 原始状态
        symmetries.append("".join(board))

        # 旋转90度
        rotated = [
            matrix[2][0],
            matrix[1][0],
            matrix[0][0],
            matrix[2][1],
            matrix[1][1],
            matrix[0][1],
            matrix[2][2],
            matrix[1][2],
            matrix[0][2],
        ]
        symmetries.append("".join(rotated))

        # 旋转180度
        rotated180 = [
            matrix[2][2],
            matrix[2][1],
            matrix[2][0],
            matrix[1][2],
            matrix[1][1],
            matrix[1][0],
            matrix[0][2],
            matrix[0][1],
            matrix[0][0],
        ]
        symmetries.append("".join(rotated180))

        # 旋转270度
        rotated270 = [
            matrix[0][2],
            matrix[1][2],
            matrix[2][2],
            matrix[0][1],
            matrix[1][1],
            matrix[2][1],
            matrix[0][0],
            matrix[1][0],
            matrix[2][0],
        ]
        symmetries.append("".join(rotated270))

        # 水平翻转
        flipped_h = [
            matrix[0][2],
            matrix[0][1],
            matrix[0][0],
            matrix[1][2],
            matrix[1][1],
            matrix[1][0],
            matrix[2][2],
            matrix[2][1],
            matrix[2][0],
        ]
        symmetries.append("".join(flipped_h))

        # 垂直翻转
        flipped_v = [
            matrix[2][0],
            matrix[2][1],
            matrix[2][2],
            matrix[1][0],
            matrix[1][1],
            matrix[1][2],
            matrix[0][0],
            matrix[0][1],
            matrix[0][2],
        ]
        symmetries.append("".join(flipped_v))

        # 主对角线翻转
        diag1 = [
            matrix[0][0],
            matrix[1][0],
            matrix[2][0],
            matrix[0][1],
            matrix[1][1],
            matrix[2][1],
            matrix[0][2],
            matrix[1][2],
            matrix[2][2],
        ]
        symmetries.append("".join(diag1))

        # 副对角线翻转
        diag2 = [
            matrix[2][2],
            matrix[1][2],
            matrix[0][2],
            matrix[2][1],
            matrix[1][1],
            matrix[0][1],
            matrix[2][0],
            matrix[1][0],
            matrix[0][0],
        ]
        symmetries.append("".join(diag2))

        return list(set(symmetries))  # 去重

    def update(self, state, action, reward, next_state, done, valid_moves):
        """更新Q值"""
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state) if next_state else None

        current_q = self.q_table[state_key][action]

        if done:
            # 游戏结束，没有下一个状态
            target = reward
        else:
            # 获取下一个状态的最大Q值（只考虑合法动作）
            next_q_values = self.q_table[next_state_key]
            valid_next_q = [next_q_values[move] for move in valid_moves]
            max_next_q = max(valid_next_q) if valid_next_q else 0
            target = reward + self.gamma * max_next_q

        # Q-learning更新公式
        self.q_table[state_key][action] = current_q + self.alpha * (target - current_q)

    def save_q_table(self, filename="q_table.pkl"):
        """保存Q表"""
        # 将defaultdict转换为普通dict以便保存
        q_table_dict = {k: v.tolist() for k, v in self.q_table.items()}
        with open(filename, "wb") as f:
            pickle.dump(q_table_dict, f)
        print(f"Q表已保存到 {filename}")

    def load_q_table(self, filename="q_table.pkl"):
        """加载Q表"""
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                q_table_dict = pickle.load(f)
            self.q_table = defaultdict(lambda: np.zeros(9))
            for k, v in q_table_dict.items():
                self.q_table[k] = np.array(v)
            print(f"Q表已从 {filename} 加载")
            return True
        return False


class RandomAgent:
    """随机智能体（用于训练对手）"""

    def __init__(self, player="O"):
        self.player = player

    def get_action(self, state, valid_moves, training=False):
        """随机选择动作"""
        return random.choice(valid_moves) if valid_moves else None


def train(episodes=10000, save_interval=1000):
    """训练Q-learning智能体"""
    env = TicTacToe()
    agent = QLearningAgent(player="X", alpha=0.1, gamma=0.9, epsilon=0.1)
    opponent = RandomAgent(player="O")

    wins = 0
    losses = 0
    draws = 0

    print("开始训练...")

    for episode in range(episodes):
        state = env.reset()
        done = False
        moves = []

        while not done:
            # 当前玩家行动
            current_agent = agent if env.current_player == "X" else opponent
            valid_moves = env.get_valid_moves()

            if not valid_moves:
                break

            action = current_agent.get_action(state, valid_moves, training=True)

            if action is None:
                break

            # 保存当前状态和动作（用于后续更新）
            if env.current_player == "X":
                moves.append((state, action, env.current_player))

            # 执行动作
            env.make_move(action)
            next_state = env.get_state()

            # 如果游戏结束，给予奖励
            if env.game_over:
                done = True
                reward = 0

                if env.winner == "X":
                    reward = 1
                    wins += 1
                elif env.winner == "O":
                    reward = -1
                    losses += 1
                else:
                    draws += 1

                # 更新智能体的Q值
                for i, (s, a, player) in enumerate(moves):
                    if player == "X":
                        # 回溯更新每一步
                        agent.update(s, a, reward, None, True, [])

            state = next_state

        # 定期保存和显示进度
        if (episode + 1) % save_interval == 0:
            win_rate = wins / (episode + 1) * 100
            print(
                f"Episode {episode + 1}: 胜率={win_rate:.1f}%, 胜={wins}, 负={losses}, 平={draws}"
            )

            # 保存Q表
            if win_rate > 50:  # 只保存胜率超过50%的模型
                agent.save_q_table(f"q_table_ep{episode+1}.pkl")

    print("训练完成！")
    agent.save_q_table()

    # 显示最终统计
    total_games = wins + losses + draws
    print(f"\n最终统计:")
    print(f"总游戏数: {total_games}")
    print(f"胜: {wins} ({wins/total_games*100:.1f}%)")
    print(f"负: {losses} ({losses/total_games*100:.1f}%)")
    print(f"平: {draws} ({draws/total_games*100:.1f}%)")

    return agent


def play_against_ai(agent, human_player="O"):
    """与AI对弈"""
    env = TicTacToe()

    print("\n" + "=" * 40)
    print("开始游戏！")
    print("你是 'O', AI是 'X'")
    print("输入0-8选择位置:")
    print(" 0 | 1 | 2 ")
    print("---+---+---")
    print(" 3 | 4 | 5 ")
    print("---+---+---")
    print(" 6 | 7 | 8 ")
    print("=" * 40)

    while not env.game_over:
        env.render()

        if env.current_player == human_player:
            # 人类玩家
            valid_moves = env.get_valid_moves()
            print(f"合法位置: {valid_moves}")

            try:
                move = int(input("请输入你的走法 (0-8): "))
                if move not in valid_moves:
                    print("无效走法！请重新选择。")
                    continue

                env.make_move(move)
            except ValueError:
                print("请输入数字！")
                continue
        else:
            # AI玩家
            valid_moves = env.get_valid_moves()
            state = env.get_state()
            move = agent.get_action(state, valid_moves, training=False)

            if move is not None:
                print(f"AI选择位置: {move}")
                env.make_move(move)

        # 检查游戏是否结束
        env.check_game_over()

    # 显示最终结果
    env.render()
    if env.winner:
        print(f"游戏结束！胜利者: {env.winner}")
    else:
        print("游戏结束！平局！")


def evaluate_ai(agent, num_games=1000):
    """评估AI性能"""
    print("\n评估AI性能...")

    opponent = RandomAgent(player="O")
    wins = 0
    losses = 0
    draws = 0

    for game in range(num_games):
        env = TicTacToe()
        state = env.reset()
        done = False

        while not done:
            current_agent = agent if env.current_player == "X" else opponent
            valid_moves = env.get_valid_moves()

            if not valid_moves:
                break

            action = current_agent.get_action(state, valid_moves, training=False)

            if action is None:
                break

            env.make_move(action)
            state = env.get_state()

            if env.game_over:
                done = True
                if env.winner == "X":
                    wins += 1
                elif env.winner == "O":
                    losses += 1
                else:
                    draws += 1

    print(f"评估结果 ({num_games} 局):")
    print(f"胜: {wins} ({wins/num_games*100:.1f}%)")
    print(f"负: {losses} ({losses/num_games*100:.1f}%)")
    print(f"平: {draws} ({draws/num_games*100:.1f}%)")


def main():
    """主函数"""
    print("子棋Q-learning算法实现")
    print("=" * 50)

    # 尝试加载已有的Q表
    agent = QLearningAgent(player="X", alpha=0.1, gamma=0.9, epsilon=0.1)
    loaded = agent.load_q_table()

    if not loaded:
        print("未找到已训练的模型，开始训练...")
        # 训练智能体
        agent = train(episodes=10000, save_interval=2000)
    else:
        print("使用已训练的模型")
        # 评估AI性能
        evaluate_ai(agent, num_games=1000)

    # 与AI对弈
    while True:
        play_against_ai(agent, human_player="O")

        again = input("\n再玩一局？ (y/n): ").lower()
        if again != "y":
            break


if __name__ == "__main__":
    main()
