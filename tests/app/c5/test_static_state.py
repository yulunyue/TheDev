"""
Test cases for StateStatic class in app.yly.envs.game.c5.model.static_state
"""
from app.yly.envs.game.c5.model.static_state import StateStatic


class TestStateStatic:
    """Test cases for StateStatic class"""
    
    def setup_method(self):
        """Setup test fixtures before each test method"""
        self.state_class = StateStatic
        self.state_class.set_board(6, 6, 4)
        self.state = self.state_class()
    
    def test_state_initialization(self):
        """Test state initialization with default values"""
        assert self.state.state == 0
        assert self.state.depth == 0
        assert self.state.player_id == 0
        assert self.state.can_moves == list(range(36))
        assert self.state.done is None
        assert hasattr(self.state, 'board')
    
    def test_class_method_set_board(self):
        """Test set_board class method"""
        # Test setting a new board configuration
        new_state = self.state_class.set_board(4, 4, 3)
        
        assert new_state.board.width == 4
        assert new_state.board.height == 4
        assert new_state.board.in_row == 3
        assert new_state.board.size == 16
    
    def test_reset_state(self):
        """Test state reset functionality"""
        # Modify state
        self.state.state = 123
        self.state.depth = 5
        self.state.player_id = 1
        
        # Reset state
        self.state.reset()
        
        # Verify reset values
        assert self.state.state == 0
        assert self.state.depth == 0
        assert self.state.player_id == 0
        assert self.state.can_moves == list(range(36))
    
    def test_set_state_integer(self):
        """Test setting state with integer value"""
        state_value = 15  # Binary: 1111 (4 pieces placed)
        self.state.set_state(state_value)
        
        assert self.state.state == state_value
        assert self.state.depth == 4  # 4 pieces placed
        assert self.state.player_id == 0  # Even depth, player 1
        assert self.state.can_moves == list(range(36))  # All positions available
    
    def test_set_state_string(self):
        """Test setting state with string value"""
        state_str = "1|2|3|4"  # 4 pieces at positions 1, 2, 3, 4
        self.state.set_state(state_str)
        
        assert self.state.state == state_str
        assert self.state.depth == 4  # 4 pieces
        assert self.state.player_id == 0  # Even depth, player 1
    
    def test_set_state_empty_string(self):
        """Test setting state with empty string"""
        self.state.set_state("")
        
        assert self.state.state == ""
        assert self.state.depth == 0
        assert self.state.player_id == 0
    
    def test_set_depth(self):
        """Test setting depth manually"""
        self.state.set_depth(3)
        
        assert self.state.depth == 3
        # Done should be None since game is not complete
        assert self.state.done is None
    
    def test_set_depth_game_complete(self):
        """Test setting depth when game is complete (board full)"""
        # Set board size to make it complete
        self.state.board.size = 4
        self.state.set_depth(4)
        
        assert self.state.depth == 4
        assert self.state.done == self.state.NO_WIN
    
    def test_get_action(self):
        """Test getting action for a position"""
        pos = 0
        action = self.state.get_action(pos)
        
        # Verify action properties
        from app.yly.envs.game.c5.model.static_action import C5ACtion
        assert isinstance(action, C5ACtion)
        assert action.action == pos
        assert action.src == self.state
        assert action.dst.player_id == 1  # Next player
        assert action.dst.depth == 1  # Depth increases by 1
    
    def test_get_action_multiple_positions(self):
        """Test getting actions for different positions"""
        action1 = self.state.get_action(0)
        action2 = self.state.get_action(1)
        action3 = self.state.get_action(35)
        
        assert action1.action == 0
        assert action2.action == 1
        assert action3.action == 35
        
        # All actions should have the same source
        assert action1.src == action2.src == action3.src == self.state
        
        # All destinations should be different
        assert action1.dst != action2.dst
        assert action2.dst != action3.dst
        assert action1.dst != action3.dst
    
    def test_make_actions(self):
        """Test generating all possible actions"""
        actions = self.state.make_actions()
        
        assert len(actions) == 36  # 6x6 board, 36 positions
        assert all(isinstance(action, C5ACtion) for action in actions)
        assert all(action.src == self.state for action in actions)
        
        # Verify all actions have unique positions
        positions = [action.action for action in actions]
        assert len(positions) == len(set(positions))  # All positions unique
    
    def test_make_actions_empty_board(self):
        """Test generating actions when board is empty"""
        # Board should already be empty in setup
        actions = self.state.make_actions()
        
        assert len(actions) == 36
        assert all(action.src.state == 0 for action in actions)
    
    def test_to_str_representation(self):
        """Test state string representation"""
        # Place some pieces for testing
        self.state.state = 15  # First 4 positions have pieces
        self.state.depth = 4
        self.state.set_state(15)
        
        # Test with algorithm scoring
        from app.yly.envs.game.c5.model.static_action import C5ACtion
        from app.yly.envs.game.c5.board.base import BoardC5
        
        # Create a mock algorithm for testing
        class MockAlgo:
            def get_action_reward(self, action):
                return 0.5 if action.action < 18 else 0.3
        
        algo = MockAlgo()
        board_str = self.state.to_str(algo)
        
        assert isinstance(board_str, list)
        assert len(board_str) == 7  # 6 rows + 1 column numbers row
        assert all(isinstance(line, str) for line in board_str)
    
    def test_to_str_no_algorithm(self):
        """Test state string representation without algorithm"""
        self.state.state = 15  # First 4 positions have pieces
        self.state.depth = 4
        self.state.set_state(15)
        
        board_str = self.state.to_str()
        
        assert isinstance(board_str, list)
        assert len(board_str) == 7
        assert all(isinstance(line, str) for line in board_str)
    
    def test_player_id_calculation(self):
        """Test player ID calculation based on depth"""
        # Test even depths (player 1)
        for depth in [0, 2, 4, 6]:
            self.state.set_depth(depth)
            assert self.state.player_id == 0
        
        # Test odd depths (player 2)
        for depth in [1, 3, 5, 7]:
            self.state.set_depth(depth)
            assert self.state.player_id == 1
    
    def test_done_state_calculation(self):
        """Test done state calculation"""
        # Test incomplete game
        self.state.board.size = 36
        self.state.set_depth(10)
        assert self.state.done is None
        
        # Test complete game (no winner)
        self.state.board.size = 4
        self.state.set_depth(4)
        assert self.state.done == self.state.NO_WIN
    
    def test_state_transfer_consistency(self):
        """Test state transfer consistency when getting actions"""
        original_state = self.state.state
        original_depth = self.state.depth
        original_player_id = self.state.player_id
        
        # Get an action
        action = self.state.get_action(5)
        
        # Original state should remain unchanged
        assert self.state.state == original_state
        assert self.state.depth == original_depth
        assert self.state.player_id == original_player_id
        
        # Destination state should be different
        assert action.dst.state != original_state
        assert action.dst.depth == original_depth + 1
        assert action.dst.player_id == 1 - original_player_id
    
    def test_can_moves_update(self):
        """Test available moves update after state changes"""
        # Initially all moves should be available
        assert len(self.state.can_moves) == 36
        assert 0 in self.state.can_moves
        assert 35 in self.state.can_moves
        
        # Create a new state with some pieces placed
        new_state = self.state_class.set_board(4, 4, 3)
        new_state.state = 15  # Some pieces placed
        new_state.set_state(15)
        
        # Verify can_moves is updated (though still all positions available in this case)
        assert isinstance(new_state.can_moves, list)
        assert len(new_state.can_moves) <= 16  # 4x4 board
    
    def test_show_titles(self):
        """Test show titles method"""
        titles = self.state.show_titles()
        
        assert isinstance(titles, str)
        assert "depth:" in titles
        assert "player:" in titles
        assert "done:" in titles
        
        # Verify depth is correct
        assert f"depth:{self.state.depth}" in titles
        # Verify player is correct
        assert f"player:{self.state.player_id+1}" in titles
        # Verify done status is included
        assert f"done:{self.state.done}" in titles