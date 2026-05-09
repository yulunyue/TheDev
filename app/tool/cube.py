from common.util.export import ApiBase, logger, Node, Dict, List
from common.tool.export import Form
from app.yly.envs.game.cube.model import CubeState, CubeAction
from app.yly.envs.game.cube.constant import C
from app.yly.envs.game.cube.algo import Al
import random


class CubeApi(ApiBase):
    ROUTE_PATH = "/cube"

    def new(self, n=2, **kw):
        C.load(n)
        s = CubeState.new_shape(n)
        return self._state_to_node(s)

    def random(self, steps=10, show_process=True, **kw):
        s = CubeState.new_shape(C.SHAPE2)
        actions_data = []
        
        for i in range(steps):
            all_actions = s.make_actions()
            action = random.choice(all_actions)
            actions_data.append({
                "step": i + 1,
                "axis": action.color,
                "layer": action.layer_id,
                "rotate": action.rotate,
                "description": action.show(),
                "state": action.dst.state,
                "grid": action.dst.grid
            })
            s = action.dst
        
        result = self._state_to_node(s)
        if show_process:
            result.childs = [Node(value=a) for a in actions_data]
        return result

    def rotate(self, state, axis, layer, rotate, **kw):
        temp_state = CubeState(state)
        actions = temp_state.make_actions()
        
        target_action = None
        for a in actions:
            if a.color == axis and a.layer_id == layer and a.rotate == rotate:
                target_action = a
                break
        
        if not target_action:
            raise Exception(f"动作不存在: axis={axis}, layer={layer}, rotate={rotate}")
        
        new_state = target_action.dst
        node = self._state_to_node(new_state)
        node.value["action"] = {
            "axis": axis,
            "layer": layer,
            "rotate": rotate,
            "description": target_action.show()
        }
        return node

    def solve(self, state, **kw):
        s = CubeState(state)
        if s.game_over():
            return Node(value={"solved": True, "actions": [], "message": "魔方已完成"})
        
        algo = Al()
        actions = algo.search_main(s)
        
        actions_data = []
        current = s
        for a in actions:
            actions_data.append({
                "axis": a.color,
                "layer": a.layer_id,
                "rotate": a.rotate,
                "description": a.show(),
                "state": a.dst.state,
                "grid": a.dst.grid
            })
            current = a.dst
        
        return Node(value={
            "solved": current.game_over(),
            "steps": len(actions),
            "actions": actions_data,
            "message": f"求解完成，共{len(actions)}步"
        })

    def get_state(self, state, **kw):
        s = CubeState(state)
        return self._state_to_node(s)

    def to_form_column_view(self, **kw):
        return Form().set_column().set_body(
            Node(value={"key": "axis", "type": "select", "label": "旋转轴", 
                      "options": ["X轴(垂直)", "Y轴(水平)", "Z轴(前后)"]}),
            Node(value={"key": "layer", "type": "select", "label": "层号",
                      "options": ["0", "1"]}),
            Node(value={"key": "rotate", "type": "select", "label": "旋转方向",
                      "options": ["-1(逆时针)", "1(顺时针)", "2(180度)"]}),
            Node(value={"key": "steps", "type": "input", "label": "打乱步数", "default": "10"}),
        )

    def _state_to_node(self, s: CubeState) -> Node:
        return Node(value={
            "state": s.state,
            "grid": s.grid,
            "n": C.n,
            "depth": s.depth,
            "game_over": s.game_over(),
            "colors": C.COLORS
        })