import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.yly.envs.game.c5.board.base import BoardC5
from app.yly.envs.game.c5.model.static_state import StateStatic
from app.yly.envs.game.c5.model.static_action import C5ACtion


class TestBoardC5:
    """测试C5游戏棋盘类"""
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        self.board = BoardC5()
        self.board.load(width=6, height=6, in_row=4)
    
    def test_board_initialization(self):
        """测试棋盘初始化"""
        assert self.board.width == 6
        assert self.board.height == 6
        assert self.board.in_row == 4
        assert self.board.size == 36
        assert len(self.board.grid) == 36
        assert all(cell == self.board.STATE_NULL for cell in self.board.grid)
    
    def test_board_reset(self):
        """测试棋盘重置"""
        # 在棋盘上放置一些棋子
        self.board.grid[0] = self.board.STATE_FIRST
        self.board.grid[1] = self.board.STATE_SECONED
        self.board.can_use = set(range(2, 36))
        
        # 重置棋盘
        self.board.reset()
        
        # 验证重置后的状态
        assert all(cell == self.board.STATE_NULL for cell in self.board.grid)
        assert self.board.can_use == set(range(36))
    
    def test_change_chess_status(self):
        """测试改变棋子状态"""
        # 测试玩家1放置棋子
        self.board.change_chess_statu(0, self.board.STATE_FIRST)
        assert self.board.grid[0] == self.board.STATE_FIRST
        assert 0 not in self.board.can_use
        
        # 测试玩家2放置棋子
        self.board.change_chess_statu(1, self.board.STATE_SECONED)
        assert self.board.grid[1] == self.board.STATE_SECONED
        assert 1 not in self.board.can_use
        
        # 测试移除棋子（设置为空）
        self.board.change_chess_statu(0, self.board.STATE_NULL)
        assert self.board.grid[0] == self.board.STATE_NULL
        assert 0 in self.board.can_use
    
    def test_put_chess(self):
        """测试放置棋子"""
        # 玩家1放置棋子
        obs = self.board.put_chess(0, self.board.STATE_FIRST)
        assert self.board.grid[0] == self.board.STATE_FIRST
        assert 0 not in self.board.can_use
        assert isinstance(obs, dict)
    
    def test_get_yx_and_get_idx(self):
        """测试坐标转换"""
        # 测试get_yx方法
        y, x = self.board.get_yx(0)
        assert y == 0, x == 0
        
        y, x = self.board.get_yx(35)
        assert y == 5, x == 5
        
        y, x = self.board.get_yx(7)
        assert y == 1, x == 1
        
        # 测试get_idx方法
        idx = self.board.get_idx(0, 0)
        assert idx == 0
        
        idx = self.board.get_idx(5, 5)
        assert idx == 35
        
        idx = self.board.get_idx(1, 1)
        assert idx == 7
    
    def test_is_valid_position(self):
        """测试位置有效性检查"""
        # 有效位置
        assert self.board.is_valide_pos(0, 0)
        assert self.board.is_valide_pos(2, 3)
        assert self.board.is_valide_pos(5, 5)
        
        # 无效位置
        assert not self.board.is_valide_pos(-1, 0)
        assert not self.board.is_valide_pos(6, 0)
        assert not self.board.is_valide_pos(0, -1)
        assert not self.board.is_valide_pos(0, 6)
    
    def test_get_next_state(self):
        """测试获取下一个状态"""
        state = 0
        new_state = self.board.get_next_state(state, 0, self.board.STATE_FIRST)
        assert new_state != state
        assert new_state == (self.board.STATE_FIRST + 1) << (0 * self.board.CHESS_SIZE)


class TestStateStatic:
    """测试C5游戏状态类"""
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        self.state_class = StateStatic
        self.state_class.set_board(6, 6, 4)
        self.state = self.state_class()
    
    def test_state_initialization(self):
        """测试状态初始化"""
        assert self.state.state == 0
        assert self.state.depth == 0
        assert self.state.player_id == 0
        assert self.state.can_moves == list(range(36))
        assert self.state.done is None
    
    def test_state_reset(self):
        """测试状态重置"""
        # 修改状态
        self.state.state = 123
        self.state.depth = 5
        self.state.player_id = 1
        
        # 重置状态
        self.state.reset()
        
        # 验证重置后的状态
        assert self.state.state == 0
        assert self.state.depth == 0
        assert self.state.player_id == 0
    
    def test_set_state_integer(self):
        """测试设置整数状态"""
        state_value = 15  # 二进制: 1111
        self.state.set_state(state_value)
        
        assert self.state.state == state_value
        assert self.state.depth == 4  # 4个棋子
        assert self.state.player_id == 0  # 偶数深度，玩家1
        assert self.state.can_moves == list(range(36))  # 所有位置都可用
    
    def test_set_state_string(self):
        """测试设置字符串状态"""
        state_str = "1|2|3|4"
        self.state.set_state(state_str)
        
        assert self.state.state == state_str
        assert self.state.depth == 4  # 4个棋子
        assert self.state.player_id == 0  # 偶数深度，玩家1
    
    def test_get_action(self):
        """测试获取动作"""
        pos = 0
        action = self.state.get_action(pos)
        
        assert isinstance(action, C5ACtion)
        assert action.action == pos
        assert action.src == self.state
        assert action.dst.player_id == 1  # 下一个玩家
        assert action.dst.depth == 1  # 深度加1
    
    def test_make_actions(self):
        """测试生成所有可能的动作"""
        actions = self.state.make_actions()
        
        assert len(actions) == 36  # 6x6棋盘，36个位置
        assert all(isinstance(action, C5ACtion) for action in actions)
        assert all(action.src == self.state for action in actions)
    
    def test_to_str(self):
        """测试状态字符串表示"""
        # 放置一些棋子
        self.state.state = 15  # 前4个位置有棋子
        self.state.depth = 4
        self.state.set_state(15)
        
        board_str = self.state.to_str()
        
        assert isinstance(board_str, list)
        assert len(board_str) == 7  # 6行棋盘 + 1行列号
        assert all(isinstance(line, str) for line in board_str)


class TestC5Action:
    """测试C5游戏动作类"""
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        self.state_class = StateStatic
        self.state_class.set_board(6, 6, 4)
        self.src_state = self.state_class()
        self.action = self.src_state.get_action(0)
    
    def test_action_initialization(self):
        """测试动作初始化"""
        assert self.action.src == self.src_state
        assert self.action.action == 0
        assert self.action.obs is None
        assert self.action.reward == 0
        assert self.action.dst is not None
    
    def test_set_obs_no_win(self):
        """测试设置观察值（无获胜情况）"""
        # 模拟放置棋子但没有获胜
        obs = {(2, 0): 1}  # 2个连续，没有对手棋子
        self.action.set_obs(obs)
        
        assert self.action.obs == obs
        assert self.action.reward == 0
        assert self.action.dst.done is None
    
    def test_set_obs_with_win(self):
        """测试设置观察值（获胜情况）"""
        # 模拟获胜情况
        obs = {(4, 0): 1}  # 4个连续，获胜
        self.action.set_obs(obs)
        
        assert self.action.obs == obs
        assert self.action.reward == 1
        assert self.action.dst.done == self.src_state.player_id + 1
    
    def test_show(self):
        """测试动作显示"""
        show_str = self.action.show()
        
        assert isinstance(show_str, str)
        assert "src:" in show_str
        assert "action:" in show_str
        assert "r:" in show_str
        assert "dst:" in show_str
        assert "obs:" in show_str


class TestC5GameIntegration:
    """测试C5游戏集成功能"""
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        self.state_class = StateStatic
        self.state_class.set_board(4, 4, 3)  # 4x4棋盘，3子连线
    
    def test_simple_game_flow(self):
        """测试简单游戏流程"""
        state = self.state_class()
        
        # 玩家1放置棋子
        action1 = state.get_action(0)
        assert action1.src.player_id == 0  # 玩家1
        
        # 玩家2放置棋子
        state = action1.dst
        action2 = state.get_action(1)
        assert action2.src.player_id == 1  # 玩家2
        
        # 验证状态转移
        assert action1.dst == action2.src
    
    def test_board_state_consistency(self):
        """测试棋盘和状态的一致性"""
        state = self.state_class()
        
        # 获取动作并执行
        action = state.get_action(5)
        new_state = action.dst
        
        # 验证状态转移正确
        assert new_state.depth == state.depth + 1
        assert new_state.player_id == 1 - state.player_id
        
        # 验证棋盘状态
        assert new_state.state != state.state
    
    def test_action_observation_reward(self):
        """测试动作的观察值和奖励"""
        state = self.state_class()
        
        # 在中心位置放置棋子
        action = state.get_action(5)  # 中心位置
        
        # 设置观察值
        obs = {(3, 1): 1}  # 3个连续，有对手棋子
        action.set_obs(obs)
        
        # 验证观察值和奖励
        assert action.obs == obs
        assert action.reward == 0  # 没有获胜
    
    def test_different_board_sizes(self):
        """测试不同棋盘大小"""
        # 测试6x6棋盘
        self.state_class.set_board(6, 6, 4)
        state_6x6 = self.state_class()
        assert state_6x6.board.size == 36
        assert len(state_6x6.can_moves) == 36
        
        # 测试4x4棋盘
        self.state_class.set_board(4, 4, 3)
        state_4x4 = self.state_class()
        assert state_4x4.board.size == 16
        assert len(state_4x4.can_moves) == 16


if __name__ == "__main__":
    pytest.main([__file__, "-v"])