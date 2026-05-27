import unittest
from unittest import SkipTest
from common.third_util.llm.opencode_client import OpencodeClient
from common.util.export import Node


class TestOpencodeClientIntegration(unittest.TestCase):
    client: OpencodeClient

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = OpencodeClient.load("csb-hcso-hcsu")
            cls.client.start_server()
        except Exception as e:
            raise SkipTest(f"Cannot setup OpencodeClient: {e}")

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_session(self):
        s = self.client.create_session(title="ut_create_session")
        self.assertIsInstance(s.id, str)
        self.assertGreater(len(s.id), 0)

    def test_execute_task(self):
        s = self.client.create_session(title="ut_exec")
        result = self.client.execute_task(s.id, "say hello")
        self.assertIsInstance(result, Node)
        self.assertTrue(result.ok)
        self.assertIsInstance(result.get_value(), str)
        self.assertGreater(len(result.get_value()), 0)

    def test_run(self):
        result = self.client.do_prompt("say hi")
        self.assertIsInstance(result, Node)
        self.assertTrue(result.ok)
        self.assertIsInstance(result.get_value(), str)
        self.assertGreater(len(result.get_value()), 0)


if __name__ == "__main__":
    unittest.main()
