from common.algo.export import encode_data
from common.util.export import ApiBase, logger, Node, Dict, List, THE_DEV_CONSTANT
from common.tool.export import Form
from app.yly.envs.game.cube.model import CubeState, CubeAction
from app.yly.envs.game.cube.constant import C
from app.yly.envs.game.cube.algo import Al
import random
from .model.cube_model import CubeModel


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
            actions_data.append(
                {
                    "step": i + 1,
                    "axis": action.axis,
                    "layer": action.layer_id,
                    "rotate": action.rotate,
                    "description": action.show(),
                    "grid": action.dst.grid,
                }
            )
            s = action.dst

        result = self._state_to_node(s)
        if show_process:
            result.childs = [Node(value=a) for a in actions_data]
        return result

    def rotate(self, grid, axis, layer, rotate, **kw):
        axis, layer, rotate = int(axis), int(layer), int(rotate)
        temp_state = CubeState(encode_data(grid, C.BIT_SIZE))
        target_action = temp_state.get_action((axis, layer, rotate))

        new_state = target_action.dst
        node = self._state_to_node(new_state)
        node.value["action"] = {
            "axis": axis,
            "layer": layer,
            "rotate": rotate,
            "description": target_action.show(),
        }
        return node

    def solve(self, grid, **kw):
        s = CubeState(encode_data(grid, C.BIT_SIZE))
        if s.game_over():
            return Node(value={"solved": True, "actions": [], "message": "魔方已完成"})

        algo = Al()
        actions = algo.search_main(s)

        actions_data = []
        current = s
        for a in actions:
            actions_data.append(
                {
                    "axis": a.axis,
                    "layer": a.layer_id,
                    "rotate": a.rotate,
                    "description": a.show(),
                    "grid": a.dst.grid,
                }
            )
            current = a.dst

        return Node(
            value={
                "solved": current.game_over(),
                "steps": len(actions),
                "actions": actions_data,
                "message": f"求解完成，共{len(actions)}步",
            }
        )

    def get_state(self, grid, **kw):
        s = CubeState(encode_data(grid, C.BIT_SIZE))
        return self._state_to_node(s)

    def scheme_rotate(self, **kw):
        return (
            Form()
            .set_body(
                CubeModel.axis,
                CubeModel.layer,
                CubeModel.rotate,
            )
            .set_btns({THE_DEV_CONSTANT.METHOD_RUN: "执行"})
        )

    def scheme_random(self, **kw):
        return (
            Form()
            .set_body(
                CubeModel.steps,
            )
            .set_btns({THE_DEV_CONSTANT.METHOD_RUN: "执行"})
        )

    def _state_to_node(self, s: CubeState) -> Node:
        return Node(
            value={
                "grid": s.grid,
                "n": C.n,
                "depth": s.depth,
                "game_over": s.game_over(),
                "colors": C.COLORS,
            }
        )
