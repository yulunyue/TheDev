import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestGitApi(unittest.TestCase):
    """测试 Git API 类"""
    
    def setUp(self):
        """设置测试环境"""
        # 导入 GitApi 类
        from common.third_service.git_tool.git_api import GitApi
        self.git_api = GitApi()
    
    def test_git_api_creation(self):
        """测试 GitApi 创建"""
        from common.third_service.git_tool.git_api import GitApi
        
        git_api = GitApi()
        self.assertIsNotNone(git_api)
        self.assertTrue(hasattr(git_api, 'repo'))
    
    @patch('common.third_service.git_tool.git_api.Repo')
    def test_clone_repository(self, mock_repo):
        """测试克隆仓库"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 模拟克隆操作
        mock_instance = MagicMock()
        mock_repo.clone_from.return_value = mock_instance
        
        git_api = GitApi()
        result = git_api.clone("https://github.com/user/repo.git", "/path/to/repo")
        
        # 验证调用
        mock_repo.clone_from.assert_called_once_with(
            "https://github.com/user/repo.git", 
            "/path/to/repo"
        )
        self.assertEqual(result, mock_instance)
    
    @patch('common.third_service.git_tool.git_api.Repo')
    def test_open_repository(self, mock_repo):
        """测试打开仓库"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 模拟仓库打开
        mock_instance = MagicMock()
        mock_repo.return_value = mock_instance
        
        git_api = GitApi()
        result = git_api.open("/path/to/repo")
        
        # 验证调用
        mock_repo.assert_called_once_with("/path/to/repo")
        self.assertEqual(result, mock_instance)
    
    def test_get_repository_info(self):
        """测试获取仓库信息"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的仓库对象
        mock_repo = MagicMock()
        mock_repo.remotes.origin.url = "https://github.com/user/repo.git"
        mock_repo.active_branch.name = "main"
        mock_repo.head.commit.hexsha = "abc123"
        mock_repo.head.commit.message = "Initial commit"
        mock_repo.head.commit.author.name = "John Doe"
        mock_repo.head.commit.author.email = "john@example.com"
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 获取仓库信息
        info = git_api.get_repo_info()
        
        # 验证返回的信息
        self.assertEqual(info['url'], "https://github.com/user/repo.git")
        self.assertEqual(info['branch'], "main")
        self.assertEqual(info['commit_hash'], "abc123")
        self.assertEqual(info['commit_message'], "Initial commit")
        self.assertEqual(info['author_name'], "John Doe")
        self.assertEqual(info['author_email'], "john@example.com")
    
    def test_get_branches(self):
        """测试获取分支列表"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的分支列表
        mock_branch1 = MagicMock()
        mock_branch1.name = "main"
        
        mock_branch2 = MagicMock()
        mock_branch2.name = "develop"
        
        mock_repo = MagicMock()
        mock_repo.branches = [mock_branch1, mock_branch2]
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 获取分支列表
        branches = git_api.get_branches()
        
        # 验证结果
        self.assertEqual(branches, ["main", "develop"])
    
    def test_get_commits(self):
        """测试获取提交历史"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的提交对象
        mock_commit1 = MagicMock()
        mock_commit1.hexsha = "abc123"
        mock_commit1.message = "Initial commit"
        mock_commit1.author.name = "John Doe"
        mock_commit1.author.email = "john@example.com"
        mock_commit1.authored_datetime.isoformat.return_value = "2023-01-01T12:00:00"
        
        mock_commit2 = MagicMock()
        mock_commit2.hexsha = "def456"
        mock_commit2.message = "Add feature"
        mock_commit2.author.name = "Jane Smith"
        mock_commit2.author.email = "jane@example.com"
        mock_commit2.authored_datetime.isoformat.return_value = "2023-01-02T12:00:00"
        
        mock_repo = MagicMock()
        mock_repo.iter_commits.return_value = [mock_commit1, mock_commit2]
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 获取提交历史
        commits = git_api.get_commits(limit=5)
        
        # 验证结果
        self.assertEqual(len(commits), 2)
        self.assertEqual(commits[0]['hash'], "abc123")
        self.assertEqual(commits[0]['message'], "Initial commit")
        self.assertEqual(commits[1]['hash'], "def456")
        self.assertEqual(commits[1]['message'], "Add feature")
    
    def test_get_files(self):
        """测试获取文件列表"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的文件对象
        mock_file1 = MagicMock()
        mock_file1.path = "src/main.py"
        
        mock_file2 = MagicMock()
        mock_file2.path = "README.md"
        
        mock_repo = MagicMock()
        mock_repo.git.ls_files.return_value = "src/main.py\nREADME.md"
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 获取文件列表
        files = git_api.get_files()
        
        # 验证结果
        self.assertEqual(len(files), 2)
        self.assertIn("src/main.py", files)
        self.assertIn("README.md", files)
    
    def test_get_file_content(self):
        """测试获取文件内容"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的 blob 对象
        mock_blob = MagicMock()
        mock_blob.data_stream.read.return_value = b"print('Hello, World!')\n"
        
        mock_repo = MagicMock()
        mock_repo.commit.return_value.tree.__getitem__.return_value = mock_blob
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 获取文件内容
        content = git_api.get_file_content("src/main.py")
        
        # 验证结果
        self.assertEqual(content, "print('Hello, World!')\n")
        
        # 验证调用
        mock_repo.commit.assert_called_once()
        mock_repo.commit.return_value.tree.__getitem__.assert_called_once_with("src/main.py")
    
    def test_create_branch(self):
        """测试创建分支"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的仓库对象
        mock_repo = MagicMock()
        mock_branch = MagicMock()
        mock_repo.create_branch.return_value = mock_branch
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 创建分支
        result = git_api.create_branch("feature-branch")
        
        # 验证结果和调用
        self.assertEqual(result, mock_branch)
        mock_repo.create_branch.assert_called_once_with("feature-branch")
    
    def test_checkout_branch(self):
        """测试切换分支"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的分支对象
        mock_branch = MagicMock()
        mock_branch.name = "feature-branch"
        
        mock_repo = MagicMock()
        mock_repo.branches.__getitem__.return_value = mock_branch
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 切换分支
        git_api.checkout("feature-branch")
        
        # 验证调用
        mock_repo.branches.__getitem__.assert_called_once_with("feature-branch")
        mock_branch.checkout.assert_called_once()
    
    def test_commit_changes(self):
        """测试提交更改"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的仓库对象
        mock_repo = MagicMock()
        mock_index = MagicMock()
        mock_commit = MagicMock()
        
        mock_repo.index = mock_index
        mock_index.commit.return_value = mock_commit
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 提交更改
        result = git_api.commit("Add new feature", "John Doe", "john@example.com")
        
        # 验证结果和调用
        self.assertEqual(result, mock_commit)
        mock_index.commit.assert_called_once_with(
            "Add new feature", 
            author="John Doe <john@example.com>"
        )
    
    def test_push_changes(self):
        """测试推送更改"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的远程对象
        mock_remote = MagicMock()
        mock_remote.push.return_value = []
        
        mock_repo = MagicMock()
        mock_repo.remotes.origin = mock_remote
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 推送更改
        git_api.push()
        
        # 验证调用
        mock_remote.push.assert_called_once()
    
    def test_pull_changes(self):
        """测试拉取更改"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的远程对象
        mock_remote = MagicMock()
        mock_remote.pull.return_value = []
        
        mock_repo = MagicMock()
        mock_repo.remotes.origin = mock_remote
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 拉取更改
        git_api.pull()
        
        # 验证调用
        mock_remote.pull.assert_called_once()
    
    def test_get_diff(self):
        """测试获取差异"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的差异对象
        mock_diff = MagicMock()
        mock_diff.diff.decode.return_value = "+print('Hello')\n-print('World')\n"
        
        mock_repo = MagicMock()
        mock_repo.git.diff.return_value = mock_diff
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        # 获取差异
        diff = git_api.get_diff("HEAD~1", "HEAD")
        
        # 验证结果
        self.assertIn("+print('Hello')", diff)
        self.assertIn("-print('World')", diff)


class TestGitApiErrorHandling(unittest.TestCase):
    """测试 GitApi 的错误处理"""
    
    def test_clone_repository_error(self):
        """测试克隆仓库时的错误处理"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 模拟克隆失败
        with patch('common.third_service.git_tool.git_api.Repo') as mock_repo:
            mock_repo.clone_from.side_effect = Exception("Clone failed")
            
            git_api = GitApi()
            with self.assertRaises(Exception):
                git_api.clone("https://github.com/user/repo.git", "/path/to/repo")
    
    def test_open_repository_error(self):
        """测试打开仓库时的错误处理"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 模拟打开失败
        with patch('common.third_service.git_tool.git_api.Repo') as mock_repo:
            mock_repo.side_effect = Exception("Repository not found")
            
            git_api = GitApi()
            with self.assertRaises(Exception):
                git_api.open("/nonexistent/path")
    
    def test_file_not_found_error(self):
        """测试文件不存在时的错误处理"""
        from common.third_service.git_tool.git_api import GitApi
        
        # 创建模拟的仓库对象
        mock_blob = MagicMock()
        mock_blob.data_stream.read.side_effect = Exception("File not found")
        
        mock_repo = MagicMock()
        mock_repo.commit.return_value.tree.__getitem__.return_value = mock_blob
        
        git_api = GitApi()
        git_api.repo = mock_repo
        
        with self.assertRaises(Exception):
            git_api.get_file_content("nonexistent/file.py")


if __name__ == '__main__':
    unittest.main()