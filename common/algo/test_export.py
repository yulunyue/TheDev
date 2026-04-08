import unittest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAlgoExport(unittest.TestCase):
    """测试算法模块的导出"""
    
    def test_import_from_export(self):
        """测试从 export 模块导入"""
        try:
            from common.algo.export import (
                PolicyIteration,
                ValueIteration,
                State,
                Action,
                AbState,
                MctsState,
                Algo,
                random_seed,
                np,
                RandomAlgo,
                MctsSearch,
                AlphaBateSearch,
                AbDev,
                Qlearning,
                Sarse,
                ALgoManage,
                Comb,
                manacher_get_odd_p,
                get_sa_prefix_doubling,
                get_height_form_sa,
                DemoState,
                Tree,
                GaussElimination,
                LazyHeapMinMax,
                LazyMinHeap,
                LazyMaxHeap,
                encode_data,
                decode_data,
                set_mask,
                get_sub_bits,
                low_bits,
                ss_or_dp,
                low_high_dp,
                Block,
                XorBais
            )
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import from algo.export: {e}")
    
    def test_basic_algorithm_classes(self):
        """测试基本算法类的导入"""
        from common.algo.export import Algo, RandomAlgo, ALgoManage
        
        # 测试类可以实例化
        algo = Algo()
        random_algo = RandomAlgo()
        algo_manage = ALgoManage()
        
        self.assertIsInstance(algo, Algo)
        self.assertIsInstance(random_algo, RandomAlgo)
        self.assertIsInstance(algo_manage, ALgoManage)
    
    def test_search_algorithm_classes(self):
        """测试搜索算法类的导入"""
        from common.algo.export import State, Action, MctsState, MctsSearch
        
        # 测试类可以实例化
        state = State()
        action = Action()
        mcts_state = MctsState()
        mcts_search = MctsSearch()
        
        self.assertIsInstance(state, State)
        self.assertIsInstance(action, Action)
        self.assertIsInstance(mcts_state, MctsState)
        self.assertIsInstance(mcts_search, MctsSearch)
    
    def test_learning_algorithm_classes(self):
        """测试学习算法类的导入"""
        from common.algo.export import PolicyIteration, ValueIteration, Qlearning, Sarse
        
        # 测试类可以实例化
        policy_iter = PolicyIteration()
        value_iter = ValueIteration()
        qlearning = Qlearning()
        sarse = Sarse()
        
        self.assertIsInstance(policy_iter, PolicyIteration)
        self.assertIsInstance(value_iter, ValueIteration)
        self.assertIsInstance(qlearning, Qlearning)
        self.assertIsInstance(sarse, Sarse)
    
    def test_math_utility_functions(self):
        """测试数学工具函数的导入"""
        from common.algo.export import sin, cos, calc_angle, sigmoid_1_to_1, sigmoid_stable
        
        # 测试函数可以调用
        import math
        
        # 测试三角函数
        self.assertAlmostEqual(sin(math.pi/2), 1.0, places=5)
        self.assertAlmostEqual(cos(math.pi), -1.0, places=5)
        
        # 测试角度计算
        self.assertGreater(calc_angle(0, 1), 0)
        
        # 测试 sigmoid 函数
        self.assertGreater(sigmoid_1_to_1(0), 0)
        self.assertLess(sigmoid_stable(1000), 1.0)
    
    def test_combinatorics_functions(self):
        """测试组合数学函数的导入"""
        from common.algo.export import manacher_get_odd_p, get_sa_prefix_doubling, get_height_form_sa, Comb
        
        # 测试组合数学类
        comb = Comb()
        self.assertIsInstance(comb, Comb)
        
        # 测试字符串处理函数
        test_str = "aba"
        result = manacher_get_odd_p(test_str)
        self.assertIsInstance(result, list)
    
    def test_tree_structure_classes(self):
        """测试树结构类的导入"""
        from common.algo.export import Tree, GaussElimination
        
        # 测试树类
        tree = Tree()
        self.assertIsInstance(tree, Tree)
        
        # 测试高斯消元类
        gauss = GaussElimination([[]], [])
        self.assertIsInstance(gauss, GaussElimination)
    
    def test_heap_structure_classes(self):
        """测试堆结构类的导入"""
        from common.algo.export import LazyHeapMinMax, LazyMinHeap, LazyMaxHeap
        
        # 测试堆类
        lazy_heap = LazyHeapMinMax()
        lazy_min_heap = LazyMinHeap()
        lazy_max_heap = LazyMaxHeap()
        
        self.assertIsInstance(lazy_heap, LazyHeapMinMax)
        self.assertIsInstance(lazy_min_heap, LazyMinHeap)
        self.assertIsInstance(lazy_max_heap, LazyMaxHeap)
    
    def test_bit_utility_functions(self):
        """测试位操作工具函数的导入"""
        from common.algo.export import encode_data, decode_data, set_mask, get_sub_bits, low_bits, ss_or_dp, low_high_dp
        
        # 测试编码解码
        data = [1, 2, 3]
        positions = [4, 4, 4]
        encoded = encode_data(data, positions)
        decoded = decode_data(encoded, positions.copy())
        self.assertEqual(decoded, data)
        
        # 测试位操作
        result = low_bits(5)  # 5 的二进制是 101，低位是 1
        self.assertIsInstance(result, list)
        self.assertIn(1, result)
        
        # 测试子集位
        subsets = get_sub_bits(3)  # 3 的二进制是 11
        self.assertIsInstance(subsets, list)
        self.assertIn(3, subsets)
    
    def test_block_structure_class(self):
        """测试块结构类的导入"""
        from common.algo.export import Block
        
        # 测试块类
        block = Block(10)
        self.assertIsInstance(block, Block)
        
        # 测试基本操作
        self.assertEqual(block.get(0), 0)
        block.update(0, 2, 5)
        self.assertEqual(block.get(2), 5)
    
    def test_xor_basis_class(self):
        """测试异或基类的导入"""
        from common.algo.export import XorBais
        
        # 测试异或基类
        xor_basis = XorBais()
        self.assertIsInstance(xor_basis, XorBais)
    
    def test_constants_and_variables(self):
        """测试常量和变量的导入"""
        from common.algo.export import random_seed, np
        
        # 测试随机种子
        self.assertIsInstance(random_seed, int)
        
        # 测试 numpy
        self.assertIsNotNone(np)
    
    def test_specialized_search_states(self):
        """测试 specialized 搜索状态的导入"""
        from common.algo.export import AbState, DemoState
        
        # 测试 Alpha-Beta 状态
        ab_state = AbState()
        self.assertIsInstance(ab_state, AbState)
        
        # 测试演示状态
        demo_state = DemoState()
        self.assertIsInstance(demo_state, DemoState)


class TestAlgoExportFunctionality(unittest.TestCase):
    """测试算法模块导出的功能"""
    
    def test_combinatorial_functions(self):
        """测试组合数学函数的功能"""
        from common.algo.export import manacher_get_odd_p
        
        # 测试 Manacher 算法
        test_cases = [
            ("aba", [0, 1, 0, 3, 0, 1, 0]),
            ("abba", [0, 1, 0, 3, 0, 5, 0]),
            ("abcba", [0, 1, 0, 3, 0, 3, 0])
        ]
        
        for s, expected in test_cases:
            with self.subTest(s=s):
                result = manacher_get_odd_p(s)
                # 验证返回的是列表
                self.assertIsInstance(result, list)
    
    def test_tree_functionality(self):
        """测试树结构的导入"""
        from common.algo.export import Tree
        
        # 测试树类的实例化
        tree = Tree()
        self.assertIsNotNone(tree)
    
    def test_gauss_elimination(self):
        """测试高斯消元类的导入"""
        from common.algo.export import GaussElimination
        
        # 简单的 2x2 方程组
        coefficients = [[2, 1], [1, 2]]
        constants = [4, 5]
        
        gauss = GaussElimination(coefficients, constants)
        self.assertIsNotNone(gauss)
    
    def test_basic_heap_operations(self):
        """测试堆结构的基本操作"""
        from common.algo.export import LazyMinHeap, LazyMaxHeap
        
        # 测试最小堆
        min_heap = LazyMinHeap()
        self.assertIsNotNone(min_heap)
        
        # 测试最大堆
        max_heap = LazyMaxHeap()
        self.assertIsNotNone(max_heap)
    
    def test_block_operations(self):
        """测试块结构的基本操作"""
        from common.algo.export import Block
        
        # 创建块结构
        block = Block(5)
        
        # 测试基本操作
        block.update(0, 4, 10)
        self.assertEqual(block.get(2), 10)
        
        # 测试范围查询
        block.update(1, 3, 5)
        self.assertEqual(block.get(1), 15)  # 10 + 5


if __name__ == '__main__':
    unittest.main()