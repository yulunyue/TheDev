"""
Test cases for C5ACtion class in app.yly.envs.game.c5.model.static_action
"""
from app.yly.envs.game.c5.model.static_action import C5ACtion
from app.yly.envs.game.c5.model.static_state import StateStatic


class TestC5ACtion:
    """Test cases for C5ACtion class"""
    
    def setup_method(self):
        """Setup test fixtures before each test method"""
        self.state_class = StateStatic
        self.state_class.set_board(6, 6, 4)
        self.src_state = self.state_class()
        self.action = self.src_state.get_action(0)
    
    def test_action_initialization(self):
        """Test action initialization with default values"""
        assert self.action.src == self.src_state
        assert self.action.action == 0
        assert self.action.obs is None
        assert self.action.reward == 0
        assert self.action.dst is not None
        assert isinstance(self.action.dst, StateStatic)
    
    def test_set_obs_no_win(self):
        """Test setting observation without win condition"""
        # Set observation without winning condition
        obs = {(2, 0): 1}  # 2 consecutive pieces, no opponent pieces
        self.action.set_obs(obs)
        
        assert self.action.obs == obs
        assert self.action.reward == 0
        assert self.action.dst.done is None
    
    def test_set_obs_with_win_all_directions(self):
        """Test setting observation with win condition (all directions)"""
        # Set observation with winning condition
        obs = {(4, 0): 1}  # 4 consecutive pieces, no opponent pieces
        self.action.set_obs(obs)
        
        assert self.action.obs == obs
        assert self.action.reward == 1
        assert self.action.dst.done == self.src_state.player_id + 1
    
    def test_set_obs_with_win_with_opponent(self):
        """Test setting observation with win condition (with opponent pieces)"""
        # Set observation with winning condition and opponent pieces
        obs = {(4, 1): 1}  # 4 consecutive pieces, with opponent pieces
        self.action.set_obs(obs)
        
        assert self.action.obs == obs
        assert self.action.reward == 1
        assert self.action.dst.done == self.src_state.player_id + 1
    
    def test_set_obs_multiple_scenarios(self):
        """Test setting observation with multiple scenarios"""
        scenarios = [
            {(3, 0): 1},  # 3 consecutive, no opponent - no win
            {(4, 0): 1},  # 4 consecutive, no opponent - win
            {(5, 0): 1},  # 5 consecutive, no opponent - win
            {(4, 1): 1},  # 4 consecutive, with opponent - win
            {(2, 1): 1},  # 2 consecutive, with opponent - no win
        ]
        
        for i, obs in enumerate(scenarios):
            test_action = self.src_state.get_action(i)
            test_action.set_obs(obs)
            
            # Check if win condition is met
            is_win = (4, 0) in obs or (4, 1) in obs or (5, 0) in obs
            expected_reward = 1 if is_win else 0
            expected_done = self.src_state.player_id + 1 if is_win else None
            
            assert test_action.reward == expected_reward
            assert test_action.dst.done == expected_done
    
    def test_show_method(self):
        """Test show method for action representation"""
        show_str = self.action.show()
        
        assert isinstance(show_str, str)
        assert "src:" in show_str
        assert "action:" in show_str
        assert "r:" in show_str
        assert "dst:" in show_str
        assert "obs:" in show_str
        
        # Verify specific content
        assert f"src:{self.src_state.state}" in show_str
        assert f"action:0,0,{self.src_state.board.s(self.src_state.player_id+1)}" in show_str
        assert "r:0" in show_str  # Initial reward is 0
    
    def test_show_with_reward(self):
        """Test show method with non-zero reward"""
        # Set a winning observation
        obs = {(4, 0): 1}
        self.action.set_obs(obs)
        
        show_str = self.action.show()
        
        assert "r:1" in show_str  # Reward should be 1
        assert f"dst:{self.action.dst.state}" in show_str
    
    def test_action_properties(self):
        """Test action properties and attributes"""
        # Test that action has all required attributes
        assert hasattr(self.action, 'src')
        assert hasattr(self.action, 'action')
        assert hasattr(self.action, 'obs')
        assert hasattr(self.action, 'reward')
        assert hasattr(self.action, 'dst')
        
        # Test attribute types
        assert isinstance(self.action.src, StateStatic)
        assert isinstance(self.action.action, int)
        assert self.action.obs is None or isinstance(self.action.obs, dict)
        assert isinstance(self.action.reward, (int, float))
        assert isinstance(self.action.dst, StateStatic)
    
    def test_action_from_different_positions(self):
        """Test actions created from different positions"""
        actions = []
        positions = [0, 5, 17, 35]  # Corner, edge, center, corner
        
        for pos in positions:
            action = self.src_state.get_action(pos)
            actions.append(action)
            
            assert action.action == pos
            assert action.src == self.src_state
            assert action.dst is not None
            assert isinstance(action.dst, StateStatic)
        
        # Verify all destinations are different
        destinations = [action.dst for action in actions]
        assert len(destinations) == len(set(destinations))
    
    def test_action_reward_reset(self):
        """Test that reward is reset when setting new observation"""
        # Set a winning observation first
        win_obs = {(4, 0): 1}
        self.action.set_obs(win_obs)
        assert self.action.reward == 1
        
        # Set a non-winning observation
        no_win_obs = {(2, 0): 1}
        self.action.set_obs(no_win_obs)
        assert self.action.reward == 0
    
    def test_observation_structure(self):
        """Test the structure of observation dictionary"""
        # Test various observation structures
        test_observations = [
            {(1, 0): 1},    # 1 consecutive, no opponent
            {(2, 1): 1},    # 2 consecutive, with opponent
            {(3, 0): 2},    # 3 consecutive, no opponent
            {(4, 1): 1},    # 4 consecutive, with opponent (win)
            {(5, 0): 1},    # 5 consecutive, no opponent (win)
        ]
        
        for obs in test_observations:
            test_action = self.src_state.get_action(1)
            test_action.set_obs(obs)
            
            assert isinstance(test_action.obs, dict)
            assert len(test_action.obs) > 0
            
            # Verify observation keys are tuples
            for key in test_action.obs.keys():
                assert isinstance(key, tuple)
                assert len(key) == 2  # (count, has_opponent)
            
            # Verify observation values are numbers
            for value in test_action.obs.values():
                assert isinstance(value, (int, float))
    
    def test_destination_state_properties(self):
        """Test properties of destination state"""
        dst_state = self.action.dst
        
        # Verify destination state properties
        assert dst_state.depth == self.src_state.depth + 1
        assert dst_state.player_id == 1 - self.src_state.player_id
        assert dst_state.state != self.src_state.state
        assert dst_state.board.width == self.src_state.board.width
        assert dst_state.board.height == self.src_state.board.height
        assert dst_state.board.in_row == self.src_state.board.in_row
    
    def test_action_immutability(self):
        """Test that action doesn't modify source state"""
        original_state = self.src_state.state
        original_depth = self.src_state.depth
        original_player_id = self.src_state.player_id
        
        # Create and modify action
        self.action.set_obs({(2, 0): 1})
        
        # Source state should remain unchanged
        assert self.src_state.state == original_state
        assert self.src_state.depth == original_depth
        assert self.src_state.player_id == original_player_id
    
    def test_multiple_actions_same_source(self):
        """Test multiple actions from the same source state"""
        actions = []
        for i in range(5):
            action = self.src_state.get_action(i)
            action.set_obs({(2, 0): 1})
            actions.append(action)
        
        # All actions should have the same source
        assert all(action.src == self.src_state for action in actions)
        
        # All actions should have different positions
        positions = [action.action for action in actions]
        assert len(positions) == len(set(positions))
        
        # All actions should have different destinations
        destinations = [action.dst for action in actions]
        assert len(destinations) == len(set(destinations))
    
    def test_action_string_representation(self):
        """Test string representation of action"""
        obs = {(3, 1): 1}  # 3 consecutive, with opponent
        self.action.set_obs(obs)
        
        show_str = self.action.show()
        
        # Verify the string contains all necessary information
        assert str(self.src_state.state) in show_str
        assert str(self.action.action) in show_str
        assert str(self.action.reward) in show_str
        assert str(self.action.dst.state) in show_str
        assert str(obs) in show_str