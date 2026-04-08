from app.tool.game import ChessF5


class TestGame:
    def test_submit_simulation(self):
        ChessF5().web_submit("simulation", dict(name="default"))
