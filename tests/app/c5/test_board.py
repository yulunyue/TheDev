"""
Test cases for BoardC5 class in app.yly.envs.game.c5.board.base
"""
from app.yly.envs.game.c5.board.base import BoardC5


class TestBoardC5:
    """Test cases for BoardC5 class"""
    
    def setup_method(self):
        """Setup test fixtures before each test method"""
        self.board = BoardC5()
        self.board.load(width=6, height=6, in_row=4)
    
    def test_board_initialization(self):
        """Test board initialization with default parameters"""
        assert self.board.width == 6
        assert self.board.height == 6
        assert self.board.in_row == 4
        assert self.board.size == 36
        assert len(self.board.grid) == 36
        assert all(cell == self.board.STATE_NULL for cell in self.board.grid)
    
    def test_board_initialization_custom(self):
        """Test board initialization with custom parameters"""
        custom_board = BoardC5()
        custom_board.load(width=4, height=4, in_row=3)
        
        assert custom_board.width == 4
        assert custom_board.height == 4
        assert custom_board.in_row == 3
        assert custom_board.size == 16
    
    def test_board_reset(self):
        """Test board reset functionality"""
        # Place some pieces on the board
        self.board.grid[0] = self.board.STATE_FIRST
        self.board.grid[1] = self.board.STATE_SECONED
        self.board.can_use = set(range(2, 36))
        
        # Reset the board
        self.board.reset()
        
        # Verify reset state
        assert all(cell == self.board.STATE_NULL for cell in self.board.grid)
        assert self.board.can_use == set(range(36))
    
    def test_change_chess_status_first_player(self):
        """Test changing chess status for first player"""
        self.board.change_chess_statu(0, self.board.STATE_FIRST)
        
        assert self.board.grid[0] == self.board.STATE_FIRST
        assert 0 not in self.board.can_use
    
    def test_change_chess_status_second_player(self):
        """Test changing chess status for second player"""
        self.board.change_chess_statu(1, self.board.STATE_SECONED)
        
        assert self.board.grid[1] == self.board.STATE_SECONED
        assert 1 not in self.board.can_use
    
    def test_change_chess_status_remove_piece(self):
        """Test removing a piece (setting to null)"""
        # First place a piece
        self.board.change_chess_statu(0, self.board.STATE_FIRST)
        assert self.board.grid[0] == self.board.STATE_FIRST
        assert 0 not in self.board.can_use
        
        # Then remove it
        self.board.change_chess_statu(0, self.board.STATE_NULL)
        assert self.board.grid[0] == self.board.STATE_NULL
        assert 0 in self.board.can_use
    
    def test_put_chess_first_player(self):
        """Test putting chess for first player"""
        obs = self.board.put_chess(0, self.board.STATE_FIRST)
        
        assert self.board.grid[0] == self.board.STATE_FIRST
        assert 0 not in self.board.can_use
        assert isinstance(obs, dict)
    
    def test_put_chess_second_player(self):
        """Test putting chess for second player"""
        obs = self.board.put_chess(1, self.board.STATE_SECONED)
        
        assert self.board.grid[1] == self.board.STATE_SECONED
        assert 1 not in self.board.can_use
        assert isinstance(obs, dict)
    
    def test_get_yx_and_get_idx_conversion(self):
        """Test coordinate conversion between index and (y, x)"""
        # Test corner positions
        y, x = self.board.get_yx(0)
        assert y == 0 and x == 0
        
        y, x = self.board.get_yx(35)
        assert y == 5 and x == 5
        
        # Test center positions
        y, x = self.board.get_yx(7)
        assert y == 1 and x == 1
        
        # Test get_idx method
        idx = self.board.get_idx(0, 0)
        assert idx == 0
        
        idx = self.board.get_idx(5, 5)
        assert idx == 35
        
        idx = self.board.get_idx(1, 1)
        assert idx == 7
    
    def test_is_valid_position_valid(self):
        """Test valid position checking"""
        # Valid positions
        assert self.board.is_valide_pos(0, 0)
        assert self.board.is_valide_pos(2, 3)
        assert self.board.is_valide_pos(5, 5)
        assert self.board.is_valide_pos(3, 1)
    
    def test_is_valid_position_invalid(self):
        """Test invalid position checking"""
        # Invalid positions - out of bounds
        assert not self.board.is_valide_pos(-1, 0)
        assert not self.board.is_valide_pos(6, 0)
        assert not self.board.is_valide_pos(0, -1)
        assert not self.board.is_valide_pos(0, 6)
        assert not self.board.is_valide_pos(-1, -1)
        assert not self.board.is_valide_pos(6, 6)
    
    def test_get_next_state(self):
        """Test getting next state after placing a piece"""
        state = 0
        pos = 0
        player_id = self.board.STATE_FIRST
        
        new_state = self.board.get_next_state(state, pos, player_id)
        
        assert new_state != state
        expected_state = (player_id + 1) << (pos * self.board.CHESS_SIZE)
        assert new_state == expected_state
    
    def test_board_representation(self):
        """Test board string representation"""
        # Place some pieces for testing
        self.board.grid[0] = self.board.STATE_FIRST
        self.board.grid[1] = self.board.STATE_SECONED
        self.board.grid[7] = self.board.STATE_FIRST
        
        # Test with score mapping
        score = {0: "W", 1: "B", 7: "Q"}
        board_str = self.board.to_str(score)
        
        assert isinstance(board_str, list)
        assert len(board_str) == 7  # 6 rows + 1 row for column numbers
        assert all(isinstance(line, str) for line in board_str)
        
        # Test without score mapping
        board_str_no_score = self.board.to_str()
        assert isinstance(board_str_no_score, list)
        assert len(board_str_no_score) == 7
    
    def test_bit_properties_initialization(self):
        """Test bit mask properties initialization"""
        assert hasattr(self.board, 'row_bit')
        assert hasattr(self.board, 'height_bit')
        assert hasattr(self.board, 'mask_cloumn')
        assert hasattr(self.board, 'mask_row')
        assert hasattr(self.board, 'mask_bit')
        
        # Verify mask values
        assert self.board.row_bit == self.board.BIT_SIZE * self.board.width
        assert self.board.height_bit == self.board.BIT_SIZE * self.board.height
        assert self.board.mask_cloumn == (1 << self.board.height_bit) - 1
        assert self.board.mask_row == (1 << self.board.row_bit) - 1
        assert self.board.mask_bit == (1 << self.board.BIT_SIZE) - 1
    
    def test_direction_constants(self):
        """Test direction constants for win checking"""
        assert hasattr(self.board, 'DR')
        assert len(self.board.DR) == 4
        # Expected directions: horizontal, vertical, diagonal down-right, diagonal down-left
        expected_directions = [[0, 1], [1, 0], [1, 1], [1, -1]]
        assert self.board.DR == expected_directions
    
    def test_player_constants(self):
        """Test player constants"""
        assert self.board.STATE_NULL == 0
        assert self.board.STATE_FIRST == 1
        assert self.board.STATE_SECONED == 2
        assert self.board.BIT_SIZE == 2
        assert self.board.CHESS_SIZE == 2
    
    def test_can_use_management(self):
        """Test available positions management"""
        # Initially all positions should be available
        assert len(self.board.can_use) == 36
        assert 0 in self.board.can_use
        assert 35 in self.board.can_use
        
        # Place a piece and verify it's removed from available positions
        self.board.put_chess(0, self.board.STATE_FIRST)
        assert 0 not in self.board.can_use
        assert len(self.board.can_use) == 35
        
        # Remove the piece and verify it's added back to available positions
        self.board.change_chess_statu(0, self.board.STATE_NULL)
        assert 0 in self.board.can_use
        assert len(self.board.can_use) == 36