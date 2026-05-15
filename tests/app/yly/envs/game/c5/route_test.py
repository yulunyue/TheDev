from common.util.export import TestBase, asset_exception
from app.yly.envs.game.c5.route import ChessF5, AI_PLAYER
from app.yly.envs.game.c5.db import Bd
from app.yly.envs.game.c5.model.chess_state import CState664
from app.yly.envs.game.c5.model.chess_state_map import CState333, CHESS_MAP_CLS_FUNC


class TestChessF5(TestBase):

    def setup_class(cls):
        Bd.instance_map = {}
        Bd._config = {}

    def setup_method(self):
        Bd.instance_map = {}
        Bd._config = {}

    def test_search_name_empty(self):
        chess = ChessF5()
        result = chess.search_name()
        assert hasattr(result, "childs")

    def test_search_algo_returns_font_search(self):
        chess = ChessF5()
        result = chess.search_algo()
        assert hasattr(result, "childs")

    def test_ai_player_set(self):
        assert "ad3" in AI_PLAYER
        assert "mc100" in AI_PLAYER

    def test_route_path(self):
        assert ChessF5.ROUTE_PATH == "/game/f5chess"

    def test_model_is_bd(self):
        assert ChessF5.model == Bd

    def test_get_not_exist(self):
        chess = ChessF5()
        asset_exception(chess.get, "not_exist_key")

    def test_get_exist_c664(self):
        c = Bd.insert(
            "test_664", name="test_664", size="C664", p0="ad3", p1="ad3", records=[]
        )
        chess = ChessF5()
        result = chess.get("test_664")
        assert result._id == "test_664"
        assert result.p0.get_value() == "ad3"
        assert result.p1.get_value() == "ad3"
        assert result.records.get_value() == []
        assert result.to_json()["width"] == 6

    def test_play_not_exist(self):
        chess = ChessF5()
        asset_exception(chess.play, "not_exist", 0, 0)

    def test_web_submit_simulation_non_ai(self):
        chess = ChessF5()
        asset_exception(
            chess.web_submit,
            "simulation",
            {"name": "sim_test", "size": "C664", "p0": "human", "p1": "human"},
        )

    def test_get_returns_correct_size_for_c664(self):
        Bd.insert(
            "test_664_size",
            name="test_664_size",
            size="C664",
            p0="ad3",
            p1="ad3",
            records=[],
        )
        chess = ChessF5()
        result = chess.get("test_664_size")
        assert result.to_json()["width"] == 6

    def test_bd_get_id(self):
        assert Bd.get_id(name="test") == "test"

    def test_bd_get_form_columns(self):
        columns = Bd.get_form_columns()
        assert len(columns) == 3

    def test_bd_insert(self):
        c = Bd.insert(
            "test_insert", name="test_insert", size="C664", p0="ad3", p1="ad3"
        )
        assert c._id == "test_insert"
        assert c.name.get_value() == "test_insert"

    def test_bd_get_state_c664(self):
        c = Bd.insert(
            "state_664", name="state_664", size="C664", p0="ad3", p1="ad3", records=[]
        )
        state = c.get_state()
        assert state.env.width == 6
        assert state.env.height == 6
        assert state.env.in_row == 4

    def test_cstate333_attributes(self):
        assert CState333.w == 3
        assert CState333.h == 3
        assert CState333.in_row == 3
        assert CState333.name == "C333"

    def test_cstate664_attributes(self):
        assert CState664.w == 6
        assert CState664.h == 6
        assert CState664.in_row == 4
        assert CState664.name == "C664"

    def test_set_board_empty(self):
        state = CState664.set_board([])
        assert state.state == 0
        assert state.depth == 0

    def test_get_can_moves_empty(self):
        state = CState664.set_board([])
        moves = state.get_can_moves()
        assert len(moves) == 36

    def test_chess_map_cls_func(self):
        assert "C664" in CHESS_MAP_CLS_FUNC
        assert "C333" in CHESS_MAP_CLS_FUNC
        assert CHESS_MAP_CLS_FUNC["C664"] == CState664
        assert CHESS_MAP_CLS_FUNC["C333"] == CState333