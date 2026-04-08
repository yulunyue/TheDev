#!/usr/bin/env python3
"""
Common 目录测试运行脚本
运行 common 目录下所有测试文件
"""

import unittest
import sys
import os
import glob
from unittest import TestLoader, TestSuite

def discover_and_run_tests():
    """发现并运行所有测试"""
    
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 查找所有测试文件
    test_files = glob.glob(os.path.join(current_dir, "**/test_*.py"), recursive=True)
    
    # 过滤掉已有的测试文件
    existing_tests = [
        "constant_test.py",
        "test_bin_util.py", 
        "test_block.py",
        "test_gauss_elim.py",
        "test_str_util.py",
        "test_node.py",
        "test_demo_state.py",
        "test_mctssearch.py",
        "test_algo.py",
        "test_git_api.py",
        "test_io.py",
        "test_gunicorn.py",
        "test_numpy.py",
        "test_pytest.py",
        "test_torch.py",
        "test_config.py",
        "test_re_util.py",
        "test_str_util.py",
        "test_thread.py",
        "test_py_file.py",
        "test_util_tool.py",
        "test_yml.py",
        "fp_test.py",
        "test_module.py",
        "test_thread_poll.py",
        "test_util_tool.py",
        "test_yml.py"
    ]
    
    # 只运行我们创建的测试文件
    our_tests = [f for f in test_files if os.path.basename(f) not in existing_tests]
    
    if not our_tests:
        print("没有找到需要运行的测试文件")
        return
    
    print(f"发现 {len(our_tests)} 个测试文件:")
    for test_file in our_tests:
        print(f"  - {test_file}")
    
    # 创建测试套件
    loader = TestLoader()
    suite = TestSuite()
    
    # 加载所有测试
    for test_file in our_tests:
        # 将文件路径转换为模块名
        module_path = os.path.relpath(test_file, current_dir).replace('\\', '/').replace('.py', '')
        module_path = f"common.{module_path}"
        
        try:
            # 动态导入测试模块
            __import__(module_path)
            module = sys.modules[module_path]
            
            # 加载测试
            test_suite = loader.loadTestsFromModule(module)
            suite.addTest(test_suite)
            
        except Exception as e:
            print(f"无法加载测试文件 {test_file}: {e}")
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果摘要
    print(f"\n测试结果摘要:")
    print(f"  运行测试数: {result.testsRun}")
    print(f"  失败数: {len(result.failures)}")
    print(f"  错误数: {len(result.errors)}")
    print(f"  跳过数: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\n错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()

def run_specific_test(test_name):
    """运行特定的测试"""
    
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建测试文件路径
    test_file = os.path.join(current_dir, test_name)
    
    if not os.path.exists(test_file):
        print(f"测试文件 {test_file} 不存在")
        return False
    
    try:
        # 动态导入测试模块
        module_path = f"common.{test_name.replace('.py', '')}"
        __import__(module_path)
        module = sys.modules[module_path]
        
        # 运行测试
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except Exception as e:
        print(f"运行测试时出错: {e}")
        return False

def main():
    """主函数"""
    
    if len(sys.argv) > 1:
        # 运行特定测试
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # 运行所有测试
        success = discover_and_run_tests()
    
    # 退出状态码
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()