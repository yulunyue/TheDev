from common.algo.base.bin_util import encode_data, decode_data, set_mask
from common.util.export import List, Dict, defaultdict, logger, log


def format(v):
    if v < 0 or v > 2:
        return "-"
    return ["-", "O", "X"][v]


class BoardC5:
    STATE_NULL = 0
    STATE_FIRST = 1
    STATE_SECONED = 2
    DR = [[0, 1], [1, 0], [1, 1], [1, -1]]

    def load(self, width, height, in_row):
        self.width, self.height, self.in_row = width, height, in_row
        self.size = self.width * self.height
        self.init_size()
        self.init_mask()
        return self

    def init_size(self):
        self.size = self.width * self.height

    def init_mask(self):
        self.mask_h = (1 << self.height) - 1
        self.mask_full = (1 << self.size) - 1
        self.mask_sets = [1 << i for i in range(self.size)]
        self.mask_clear = [self.mask_full ^ (1 << i) for i in range(self.size)]
        self.set_state(0)
        return self

    def put_chess(self, idx, player_id):
        if player_id == 0:
            self.state_pos &= self.mask_clear[idx]
            self.state_statu &= self.mask_clear[idx]
            return self
        self.state_pos |= self.mask_sets[idx]
        if player_id & 2:
            self.state_statu &= self.mask_clear[idx]
        else:
            self.state_statu |= self.mask_sets[idx]
        return self

    def set_state_any(self, state):
        if isinstance(state, int):
            self.set_state(state)
        elif isinstance(state, str):
            self.change_grid(state)
        elif isinstance(state, list):
            self.load_records(state)
        return self

    def set_state(self, state: int):
        self.state_pos = state >> self.size
        self.state_statu = state ^ (self.state_pos << self.size)
        return self

    def get_state(self):
        return (self.state_pos << self.size) | self.state_statu

    def change_grid(self, s: str):
        self.set_state(0)
        for i, v in enumerate(s.split("|")):
            self.put_chess(int(v), (i % 2) + 1)

    def to_str(self, score: dict):
        ret = [[f"{i}"] + [" "] * self.width for i in range(self.height)]
        for idx in range(self.size):
            y, x = idx % self.height, idx // self.width
            s = 0
            if self.state_pos & self.mask_sets[idx]:
                s = 1 if self.state_statu & self.mask_sets[idx] else 2
            ret[y][x + 1] = format(s)
        # 在棋盘上显示评分
        if score:
            for (y, x), s in score.items():
                if 0 <= y < self.height and 0 <= x < self.width:
                    idx = y * self.width + x
                    if not (self.state_pos & self.mask_sets[idx]):  # 只在空位显示评分
                        ret[y][x + 1] = f"{s:.1f}"
        ret.append([" "] + [str(v) for v in range(self.width)])
        return [" ".join(row) for row in ret]

    def load_records(self, records):
        self.set_state(0)
        for i, idx in enumerate(records):
            self.put_chess(idx, (i % 2) + self.STATE_FIRST)
        return self

    # ========== 胜负判断功能 ==========
    
    def check_win(self, idx, player_id):
        """检查在指定位置落子后是否获胜"""
        if not (self.state_pos & self.mask_sets[idx]):  # 位置为空
            return False
            
        # 获取棋子坐标
        y = idx // self.width
        x = idx % self.width
        
        # 检查四个方向
        for dy, dx in self.DR:
            if self._check_line_win(y, x, dy, dx, player_id):
                return True
        
        return False
    
    def _check_line_win(self, y, x, dy, dx, player_id):
        """检查从指定位置开始，某个方向上是否达到获胜条件"""
        # 确定玩家的状态位
        if player_id == 1:
            player_mask = 1
        else:
            player_mask = 0
        
        count = 1  # 包括当前位置
        
        # 正向检查
        ny, nx = y + dy, x + dx
        while 0 <= ny < self.height and 0 <= nx < self.width:
            idx = ny * self.width + nx
            if self.state_pos & self.mask_sets[idx]:
                if player_id == 1:
                    if self.state_statu & self.mask_sets[idx]:
                        count += 1
                        ny += dy
                        nx += dx
                    else:
                        break
                else:  # player_id == 2
                    if not (self.state_statu & self.mask_sets[idx]):
                        count += 1
                        ny += dy
                        nx += dx
                    else:
                        break
            else:
                break
        
        # 反向检查
        ny, nx = y - dy, x - dx
        while 0 <= ny < self.height and 0 <= nx < self.width:
            idx = ny * self.width + nx
            if self.state_pos & self.mask_sets[idx]:
                if player_id == 1:
                    if self.state_statu & self.mask_sets[idx]:
                        count += 1
                        ny -= dy
                        nx -= dx
                    else:
                        break
                else:  # player_id == 2
                    if not (self.state_statu & self.mask_sets[idx]):
                        count += 1
                        ny -= dy
                        nx -= dx
                    else:
                        break
            else:
                break
        
        return count >= self.in_row
    
    def get_winner(self):
        """获取当前棋盘的获胜者"""
        # 遍历所有棋子位置，检查是否有获胜者
        for idx in range(self.size):
            if self.state_pos & self.mask_sets[idx]:
                # 检查玩家1是否获胜
                if self.state_statu & self.mask_sets[idx]:
                    if self.check_win(idx, 1):
                        return 1
                # 检查玩家2是否获胜
                else:
                    if self.check_win(idx, 2):
                        return 2
        
        # 检查是否平局
        if self.state_pos == self.mask_full:
            return 0
        
        # 游戏未结束
        return -1
    
    def is_game_over(self):
        """检查游戏是否结束"""
        return self.get_winner() != -1

    # ========== 单步评分功能 ==========
    
    def evaluate_move(self, idx, player_id):
        """评估在指定位置落子的分数"""
        if self.state_pos & self.mask_sets[idx]:  # 位置已有棋子
            return -float('inf')
        
        # 模拟落子
        original_pos = self.state_pos
        original_statu = self.state_statu
        
        self.put_chess(idx, player_id)
        
        score = self._evaluate_position(idx, player_id)
        
        # 恢复状态
        self.state_pos = original_pos
        self.state_statu = original_statu
        
        return score
    
    def _evaluate_position(self, idx, player_id):
        """评估某个位置的分数"""
        score = 0
        
        # 获取坐标
        y = idx // self.width
        x = idx % self.width
        
        # 检查四个方向
        for dy, dx in self.DR:
            line_score = self._evaluate_line(y, x, dy, dx, player_id)
            score += line_score
        
        # 中心位置加分
        center_y, center_x = self.height // 2, self.width // 2
        distance_to_center = abs(y - center_y) + abs(x - center_x)
        score += (self.height + self.width - distance_to_center) * 0.1
        
        return score
    
    def _evaluate_line(self, y, x, dy, dx, player_id):
        """评估某个方向的分数"""
        # 确定玩家的状态位
        if player_id == 1:
            player_mask = 1
        else:
            player_mask = 0
        
        # 获取该方向上的连续棋子数和空位
        line_info = self._get_line_info(y, x, dy, dx, player_id)
        
        # 根据连续棋子数和空位评分
        return self._score_line_pattern(line_info)
    
    def _get_line_info(self, y, x, dy, dx, player_id):
        """获取某个方向上的棋子信息"""
        player_mask = 1 if player_id == 1 else 0
        
        # 检查两个方向上的连续棋子
        my_count = 1  # 包括当前位置
        empty_count = 0
        blocked_count = 0
        
        # 正向检查
        ny, nx = y + dy, x + dx
        while 0 <= ny < self.height and 0 <= nx < self.width and my_count + empty_count < self.in_row:
            idx = ny * self.width + nx
            if self.state_pos & self.mask_sets[idx]:
                if player_id == 1:
                    if self.state_statu & self.mask_sets[idx]:
                        my_count += 1
                    else:
                        blocked_count += 1
                        break
                else:  # player_id == 2
                    if not (self.state_statu & self.mask_sets[idx]):
                        my_count += 1
                    else:
                        blocked_count += 1
                        break
            else:
                empty_count += 1
                break
            ny += dy
            nx += dx
        
        # 反向检查
        ny, nx = y - dy, x - dx
        while 0 <= ny < self.height and 0 <= nx < self.width and my_count + empty_count < self.in_row:
            idx = ny * self.width + nx
            if self.state_pos & self.mask_sets[idx]:
                if player_id == 1:
                    if self.state_statu & self.mask_sets[idx]:
                        my_count += 1
                    else:
                        blocked_count += 1
                        break
                else:  # player_id == 2
                    if not (self.state_statu & self.mask_sets[idx]):
                        my_count += 1
                    else:
                        blocked_count += 1
                        break
            else:
                empty_count += 1
                break
            ny -= dy
            nx -= dx
        
        return {
            'my_count': my_count,
            'empty_count': empty_count,
            'blocked_count': blocked_count,
            'total_count': my_count + empty_count
        }
    
    def _score_line_pattern(self, line_info):
        """根据棋子模式评分"""
        my_count = line_info['my_count']
        empty_count = line_info['empty_count']
        blocked_count = line_info['blocked_count']
        
        # 如果没有足够的空位，无法形成五子连珠
        if my_count + empty_count < self.in_row:
            return 0
        
        # 根据连续棋子数评分
        if my_count >= self.in_row:
            return 100000  # 必胜
        
        # 活四：4个连续棋子，两边有空位
        if my_count == 4 and empty_count == 2 and blocked_count == 0:
            return 10000
        
        # 冲四：4个连续棋子，一边被堵
        if my_count == 4 and empty_count == 1 and blocked_count == 1:
            return 1000
        
        # 活三：3个连续棋子，两边有空位
        if my_count == 3 and empty_count == 3 and blocked_count == 0:
            return 1000
        
        # 眠三：3个连续棋子，一边被堵
        if my_count == 3 and empty_count == 2 and blocked_count == 1:
            return 100
        
        # 活二：2个连续棋子，两边有空位
        if my_count == 2 and empty_count == 4 and blocked_count == 0:
            return 100
        
        # 眠二：2个连续棋子，一边被堵
        if my_count == 2 and empty_count == 3 and blocked_count == 1:
            return 10
        
        # 单子
        if my_count == 1:
            return 1
        
        return 0

    # ========== 局面评分功能 ==========
    
    def evaluate_board(self, player_id):
        """评估整个棋盘对某个玩家的分数"""
        opponent_id = 3 - player_id  # 对手玩家
        
        my_score = 0
        opponent_score = 0
        
        # 遍历所有空位，评估每个位置的分数
        for idx in range(self.size):
            if not (self.state_pos & self.mask_sets[idx]):
                my_move_score = self.evaluate_move(idx, player_id)
                opponent_move_score = self.evaluate_move(idx, opponent_id)
                
                # 只考虑正分数的移动
                if my_move_score > 0:
                    my_score += my_move_score
                if opponent_move_score > 0:
                    opponent_score += opponent_move_score
        
        # 如果对手有必胜走法，给予极大惩罚
        if opponent_score >= 100000:
            return -float('inf')
        
        # 如果我有必胜走法，给予极大奖励
        if my_score >= 100000:
            return float('inf')
        
        # 综合评分：我的分数减去对手的分数
        # 给对手的分数更高权重，因为防守更重要
        return my_score - opponent_score * 1.2
    
    def get_best_move(self, player_id):
        """获取最佳走法"""
        best_score = -float('inf')
        best_move = -1
        score_dict = {}
        
        # 遍历所有空位
        for idx in range(self.size):
            if not (self.state_pos & self.mask_sets[idx]):
                # 评估这个位置的分数
                score = self.evaluate_move(idx, player_id)
                
                # 转换为坐标
                y = idx // self.width
                x = idx % self.width
                
                score_dict[(y, x)] = score
                
                # 更新最佳走法
                if score > best_score:
                    best_score = score
                    best_move = idx
        
        return best_move, best_score, score_dict
    
    def get_move_scores(self, player_id):
        """获取所有走法的评分"""
        score_dict = {}
        
        # 遍历所有空位
        for idx in range(self.size):
            if not (self.state_pos & self.mask_sets[idx]):
                # 评估这个位置的分数
                score = self.evaluate_move(idx, player_id)
                
                # 转换为坐标
                y = idx // self.width
                x = idx % self.width
                
                score_dict[(y, x)] = score
        
        return score_dict