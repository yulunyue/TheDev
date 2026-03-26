"""
Integration tests for C5 game module
"""
from app.yly.envs.game.c5.board.base import BoardC5
from app.yly.envs.game.c5.model.static_state import StateStatic
from app.yly.envs.game.c5.model.static_action import C5ACtion


class TestC5GameIntegration:
    """Integration tests for C5 game functionality"""
    
    def setup_method(self):
        """Setup test fixtures before each test method"""
        self.state_class = StateStatic
    
    def test_simple_game_flow_4x4(self):
        """Test simple game flow on 4x4 board"""
        # Setup 4x4 board with 3-in-a-row win condition
        self.state_class.set_board(4, 4, 3)
        state = self.state_class()
        
        # Player 1 places piece at position 0
        action1 = state.get_action(0)
        assert action1.src.player_id == 0  # Player 1
        assert action1.action == 0
        
        # Player 2 places piece at position 1
        state_after_1 = action1.dst
        action2 = state_after_1.get_action(1)
        assert action2.src.player_id == 1  # Player 2
        assert action2.action == 1
        
        # Verify state transition
        assert action1.dst == action2.src
        assert action2.dst.depth == 2  # Two moves made
        
    def test_simple_game_flow_6x6(self):
        """Test simple game flow on 6x6 board"""
        # Setup 6x6 board with 4-in-a-row win condition
        self.state_class.set_board(6, 6, 4)
        state = self.state_class()
        
        # Simulate a sequence of moves
        moves = [0, 1, 6, 7, 12, 13]  # Simple diagonal pattern
        
        current_state = state
        for i, move in enumerate(moves):
            action = current_state.get_action(move)
            assert action.action == move
            assert action.src.player_id == i % 2  # Alternate players
            
            if i < len(moves) - 1:
                current_state = action.dst
                assert current_state.depth == i + 1
    
    def test_board_state_consistency(self):
        """Test consistency between board and state"""
        # Setup board
        self.state_class.set_board(4, 4, 3)
        state = self.state_class()
        
        # Get action and execute it
        action = state.get_action(5)  # Center position
        new_state = action.dst
        
        # Verify state transition properties
        assert new_state.depth == state.depth + 1
        assert new_state.player_id == 1 - state.player_id
        assert new_state.state != state.state
        
        # Verify board properties are consistent
        assert new_state.board.width == state.board.width
        assert new_state.board.height == state.board.height
        assert new_state.board.in_row == state.board.in_row
        assert new_state.board.size == state.board.size
        
        # Verify move is recorded in board
        # The position should be occupied in the new state
        assert new_state.board.grid[5] == state.player_id + 1  # Player's piece
    
    def test_action_observation_reward_workflow(self):
        """Test complete action observation reward workflow"""
        # Setup board
        self.state_class.set_board(4, 4, 3)
        state = self.state_class()
        
        # Place pieces in a line to test win condition
        center_pos = 5  # Center position in 4x4 board
        
        # Place first piece
        action1 = state.get_action(center_pos)
        obs1 = {(2, 0): 1}  # 2 consecutive, no opponent
        action1.set_obs(obs1)
        
        # Move to next state
        state2 = action1.dst
        
        # Place second piece adjacent
        action2 = state2.get_action(center_pos + 1)
        obs2 = {(3, 0): 1}  # 3 consecutive, no opponent
        action2.set_obs(obs2)
        
        # Move to next state
        state3 = action2.dst
        
        # Place third piece to win
        action3 = state3.get_action(center_pos + 2)
        obs3 = {(4, 0): 1}  # 4 consecutive, win condition
        action3.set_obs(obs3)
        
        # Verify win condition
        assert action3.reward == 1
        assert action3.dst.done == state3.player_id + 1
    
    def test_different_board_sizes_integration(self):
        """Test integration with different board sizes"""
        board_configs = [
            (4, 4, 3),  # 4x4 board, 3-in-a-row
            (6, 6, 4),  # 6x6 board, 4-in-a-row
            (10, 10, 5),  # 10x10 board, 5-in-a-row
        ]
        
        for width, height, in_row in board_configs:
            # Setup board configuration
            self.state_class.set_board(width, height, in_row)
            state = self.state_class()
            
            # Test basic properties
            assert state.board.width == width
            assert state.board.height == height
            assert state.board.in_row == in_row
            assert state.board.size == width * height
            assert len(state.can_moves) == width * height
            
            # Test action generation
            actions = state.make_actions()
            assert len(actions) == width * height
            
            # Test a simple move
            action = state.get_action(0)
            assert action.action == 0
            assert action.dst.depth == 1
            assert action.dst.player_id == 1
    
    def test_full_board_scenario(self):
        """Test scenario where board becomes full"""
        # Setup small board to test fill scenario
        self.state_class.set_board(2, 2, 2)  # 2x2 board, 2-in-a-row
        state = self.state_class()
        
        # Fill the board completely
        moves = [0, 1, 2, 3]  # All positions
        current_state = state
        
        for i, move in enumerate(moves):
            action = current_state.get_action(move)
            current_state = action.dst
            
            # Check if game is complete
            if current_state.board.size == current_state.depth:
                assert current_state.done == current_state.NO_WIN
    
    def test_win_detection_integration(self):
        """Test win detection integration"""
        # Setup board
        self.state_class.set_board(4, 4, 3)
        state = self.state_class()
        
        # Create a winning scenario (horizontal)
        winning_moves = [0, 1, 2]  # First row
        
        current_state = state
        for move in winning_moves:
            action = current_state.get_action(move)
            # Set observation to simulate consecutive pieces
            obs = {(len(winning_moves), 0): 1}  # All consecutive, no opponent
            action.set_obs(obs)
            current_state = action.dst
        
        # The last move should trigger win
        final_action = current_state.get_action(3)  # Complete the row
        win_obs = {(4, 0): 1}  # 4 consecutive pieces
        final_action.set_obs(win_obs)
        
        assert final_action.reward == 1
        assert final_action.dst.done == current_state.player_id + 1
    
    def test_state_serialization_roundtrip(self):
        """Test state serialization and deserialization"""
        # Setup board
        self.state_class.set_board(4, 4, 3)
        original_state = self.state_class()
        
        # Make some moves
        action1 = original_state.get_action(0)
        action2 = action1.dst.get_action(1)
        
        # Test integer state
        int_state = action2.dst.state
        assert isinstance(int_state, int)
        
        # Test string state
        str_state = "0|1|2|3"
        string_state_obj = self.state_class()
        string_state_obj.set_state(str_state)
        
        assert string_state_obj.state == str_state
        assert string_state_obj.depth == 4
        assert string_state_obj.player_id == 0  # Even depth
        
        # Test state consistency after string serialization
        assert string_state_obj.can_moves == list(range(16))  # All positions available
    
    def test_action_chain_consistency(self):
        """Test consistency of action chains"""
        # Setup board
        self.state_class.set_board(4, 4, 3)
        initial_state = self.state_class()
        
        # Create a chain of actions
        actions = []
        current_state = initial_state
        
        for i in range(5):  # Make 5 moves
            action = current_state.get_action(i)
            action.set_obs({(1, 0): 1})  # Single piece, no opponent
            actions.append(action)
            current_state = action.dst
        
        # Verify chain consistency
        for i in range(len(actions) - 1):
            assert actions[i].dst == actions[i + 1].src
        
        # Verify final state properties
        final_state = current_state
        assert final_state.depth == 5
        assert final_state.player_id == 1  # Odd depth
        assert final_state.state != initial_state.state
    
    def test_board_display_integration(self):
        """Test board display functionality integration"""
        # Setup board
        self.state_class.set_board(4, 4, 3)
        state = self.state_class()
        
        # Place some pieces
        pieces_to_place = [0, 1, 4, 5]  # Top-left 2x2 area
        
        current_state = state
        for piece in pieces_to_place:
            action = current_state.get_action(piece)
            action.set_obs({(1, 0): 1})
            current_state = action.dst
        
        # Test board display
        board_str = current_state.to_str()
        
        assert isinstance(board_str, list)
        assert len(board_str) == 5  # 4 rows + 1 column numbers row
        assert all(isinstance(line, str) for line in board_str)
        
        # Test display with scoring
        class MockAlgo:
            def get_action_reward(self, action):
                return float(action.action) / 16.0
        
        scored_board_str = current_state.to_str(MockAlgo())
        assert isinstance(scored_board_str, list)
        assert len(scored_board_str) == 5
    
    def test_error_handling_integration(self):
        """Test error handling in integration scenarios"""
        # Setup board
        self.state_class.set_board(4, 4, 3)
        state = self.state_class()
        
        # Test getting action for invalid position (should not raise error in normal flow)
        # This tests that the action system handles edge cases gracefully
        action = state.get_action(0)  # Valid position
        assert action is not None
        
        # The action system should handle observations properly
        # even with various input types
        test_observations = [
            {(1, 0): 1},
            {(2, 1): 1},
            {(3, 0): 1},
            {},  # Empty observation
        ]
        
        for obs in test_observations:
            test_action = state.get_action(1)
            test_action.set_obs(obs)
            assert test_action.obs == obs