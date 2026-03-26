"""
Simple test runner for C5 game module
"""
import sys
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Add app directory to path for module importing
app_path = project_root / "app"
sys.path.insert(0, str(app_path))

def run_test_function(test_func):
    """Run a single test function and return result"""
    try:
        test_func()
        return True, None
    except Exception as e:
        return False, str(e)

def run_test_class(test_class):
    """Run all test methods in a test class"""
    try:
        class_instance = test_class()
        test_methods = [method for method in dir(class_instance) 
                       if method.startswith('test_')]
        
        results = []
        for method_name in test_methods:
            method = getattr(class_instance, method_name)
            passed, error = run_test_function(method)
            results.append({
                'method': method_name,
                'passed': passed,
                'error': error
            })
        
        return results
    except Exception as e:
        return [{'method': f'{test_class.__name__}__init__', 'passed': False, 'error': str(e)}]

def run_test_file(file_name):
    """Run all test classes in a test file"""
    try:
        # Import the module directly
        module = __import__(file_name)
        
        test_classes = [getattr(module, name) for name in dir(module) 
                       if name.startswith('Test') and hasattr(getattr(module, name), '__dict__')]
        
        all_results = []
        for test_class in test_classes:
            class_results = run_test_class(test_class)
            all_results.extend(class_results)
        
        return all_results
    except Exception as e:
        return [{'method': f'文件导入_{file_name}', 'passed': False, 'error': str(e)}]

def main():
    """Main test runner"""
    print("=" * 60)
    print("C5游戏模块测试运行器")
    print("=" * 60)
    
    # Test files to run
    test_files = [
        "test_board",
        "test_static_state", 
        "test_static_action",
        "test_integration"
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    failed_details = []
    
    for test_file in test_files:
        print(f"\n📁 运行测试文件: {test_file}.py")
        print("-" * 40)
        
        try:
            # Import test module
            test_module = __import__(test_file)
            
            # Get test classes
            test_classes = [getattr(test_module, name) for name in dir(test_module) 
                           if name.startswith('Test') and hasattr(getattr(test_module, name), '__dict__')]
            
            file_passed = 0
            file_failed = 0
            
            for test_class in test_classes:
                class_name = test_class.__name__
                print(f"  🧪 测试类: {class_name}")
                
                try:
                    class_instance = test_class()
                    test_methods = [method for method in dir(class_instance) 
                                   if method.startswith('test_')]
                    
                    for method_name in test_methods:
                        method = getattr(class_instance, method_name)
                        passed, error = run_test_function(method)
                        
                        total_tests += 1
                        if passed:
                            passed_tests += 1
                            file_passed += 1
                            print(f"    ✅ {method_name}")
                        else:
                            failed_tests += 1
                            file_failed += 1
                            print(f"    ❌ {method_name}: {error}")
                            failed_details.append({
                                'file': test_file,
                                'class': class_name,
                                'method': method_name,
                                'error': error
                            })
                except Exception as e:
                    total_tests += 1
                    failed_tests += 1
                    file_failed += 1
                    error_msg = f"类初始化失败: {str(e)}"
                    print(f"    ❌ {class_name}: {error_msg}")
                    failed_details.append({
                        'file': test_file,
                        'class': class_name,
                        'method': '类初始化',
                        'error': error_msg
                    })
            
            print(f"  📊 文件结果: {file_passed} 通过, {file_failed} 失败")
            
        except Exception as e:
            print(f"  💥 文件运行失败: {e}")
            traceback.print_exc()
            failed_details.append({
                'file': test_file,
                'class': '文件导入',
                'method': '导入',
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 测试结果汇总")
    print("=" * 60)
    print(f"📊 总测试数: {total_tests}")
    print(f"✅ 通过: {passed_tests}")
    print(f"❌ 失败: {failed_tests}")
    print(f"📈 成功率: {passed_tests/total_tests*100:.1f}%" if total_tests > 0 else "0%")
    
    if failed_tests > 0:
        print(f"\n❌ 失败详情:")
        for detail in failed_details:
            print(f"   📁 {detail['file']}::{detail['class']}::{detail['method']}")
            print(f"   💥 {detail['error']}")
    
    # Return exit code
    if failed_tests == 0:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️  有 {failed_tests} 个测试失败")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)