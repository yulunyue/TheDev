#!/usr/bin/env python3
"""
Test runner for C5 game module - No unittest dependency
Run all tests in the c5 test suite
"""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))
sys.path.insert(0, project_root)


def run_test_module(module_name, test_function):
    """Run a specific test module"""
    print(f"\n🚀 Running {module_name}...")
    try:
        success = test_function()
        if success:
            print(f"✅ {module_name} - All tests passed!")
            return True
        else:
            print(f"❌ {module_name} - Some tests failed!")
            return False
    except Exception as e:
        print(f"❌ {module_name} - Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_c5_tests():
    """Run all C5 game tests"""
    print("🚀 Starting C5 Game Test Suite")
    print("=" * 60)
    
    # Import test functions
    try:
        from tests.app.yly.envs.game.c5.board.test_base import run_board_tests
        from tests.app.yly.envs.game.c5.model.test_static_state import run_model_tests
        from tests.app.yly.envs.game.c5.player.test_players import run_player_tests
        from tests.app.yly.envs.game.c5.test_c5_integration import run_integration_tests
    except Exception as e:
        print(f"❌ Failed to import test modules: {e}")
        return False
    
    # Run test modules
    test_modules = [
        ("Board Module Tests", run_board_tests),
        ("Model Module Tests", run_model_tests),
        ("Player Module Tests", run_player_tests),
        ("Integration Tests", run_integration_tests),
    ]
    
    passed = 0
    total = len(test_modules)
    
    for module_name, test_func in test_modules:
        try:
            if run_test_module(module_name, test_func):
                passed += 1
        except Exception as e:
            print(f"❌ {module_name} execution error: {e}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Overall Test Results Summary")
    print(f"   Test modules run: {total}")
    print(f"   Passed: {passed}")
    print(f"   Failed: {total - passed}")
    print(f"   Success rate: {(passed / total * 100):.1f}%")
    
    if passed == total:
        print("🎉 All test modules passed!")
        return True
    else:
        print("💥 Some test modules failed!")
        return False


def run_specific_test(test_module_name):
    """Run a specific test module"""
    test_modules = {
        'board': 'tests.app.yly.envs.game.c5.board.test_base',
        'model': 'tests.app.yly.envs.game.c5.model.test_static_state',
        'player': 'tests.app.yly.envs.game.c5.player.test_players',
        'integration': 'tests.app.yly.envs.game.c5.test_c5_integration',
    }
    
    if test_module_name not in test_modules:
        print(f"❌ Unknown test module: {test_module_name}")
        print(f"Available modules: {list(test_modules.keys())}")
        return False
    
    module_path = test_modules[test_module_name]
    
    try:
        # Dynamic import and execution
        if test_module_name == 'board':
            from tests.app.yly.envs.game.c5.board.test_base import run_board_tests
            return run_board_tests()
        elif test_module_name == 'model':
            from tests.app.yly.envs.game.c5.model.test_static_state import run_model_tests
            return run_model_tests()
        elif test_module_name == 'player':
            from tests.app.yly.envs.game.c5.player.test_players import run_player_tests
            return run_player_tests()
        elif test_module_name == 'integration':
            from tests.app.yly.envs.game.c5.test_c5_integration import run_integration_tests
            return run_integration_tests()
    except Exception as e:
        print(f"❌ Failed to run {test_module_name} tests: {e}")
        return False


def print_help():
    """Print help information"""
    print("C5 Game Test Runner - No unittest dependency")
    print("=" * 50)
    print("Usage:")
    print("  python run_all_tests.py                    # Run all tests")
    print("  python run_all_tests.py --module board     # Run board tests only")
    print("  python run_all_tests.py --module model     # Run model tests only")
    print("  python run_all_tests.py --module player    # Run player tests only")
    print("  python run_all_tests.py --module integration  # Run integration tests only")
    print("  python run_all_tests.py --help             # Show this help")
    print()
    print("Available test modules:")
    print("  board      - Board module tests")
    print("  model      - Model module tests")
    print("  player     - Player module tests")
    print("  integration - Integration tests")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='C5 Game Test Runner - No unittest dependency')
    parser.add_argument('--module', '-m', type=str, 
                       choices=['board', 'model', 'player', 'integration'],
                       help='Run specific test module')
    parser.add_argument('--help', '-h', action='store_true',
                       help='Show help information')
    
    args = parser.parse_args()
    
    if args.help:
        print_help()
    elif args.module:
        success = run_specific_test(args.module)
    else:
        success = run_all_c5_tests()
    
    sys.exit(0 if success else 1)