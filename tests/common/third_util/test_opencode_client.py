import unittest
from unittest import SkipTest
from common.third_util.llm.opencode_client import OpencodeClient
from common.third_util.llm.opencode_db import OpencodeDb
from common.util.export import Node


class TestOpencodeClientParse(unittest.TestCase):
    def test_parse_messages(self):
        messages = [
            {
                "info": {"role": "user", "time": {"created": 1000}},
                "parts": [{"type": "text", "text": "hello"}],
            },
            {
                "info": {"role": "assistant", "time": {"created": 2000}},
                "parts": [
                    {"type": "text", "text": "hi there"},
                    {
                        "type": "tool",
                        "call_id": "call_001",
                        "tool": "read",
                        "state": {"input": {}, "output": "file content"},
                    },
                ],
            },
        ]
        text, tool_parts = OpencodeClient._parse_messages(messages)
        self.assertEqual(text, "hi there")
        self.assertEqual(len(tool_parts), 1)
        self.assertEqual(tool_parts[0]["tool"], "read")

    def test_parse_messages_no_assistant(self):
        messages = [
            {
                "info": {"role": "user", "time": {"created": 1000}},
                "parts": [{"type": "text", "text": "hello"}],
            },
        ]
        text, tool_parts = OpencodeClient._parse_messages(messages)
        self.assertEqual(text, "")
        self.assertEqual(len(tool_parts), 0)

    def test_parse_messages_multiple_tools(self):
        messages = [
            {
                "info": {"role": "assistant", "time": {"created": 1000}},
                "parts": [
                    {
                        "type": "tool",
                        "call_id": "call_001",
                        "tool": "read",
                        "state": {},
                    },
                    {
                        "type": "tool",
                        "call_id": "call_002",
                        "tool": "write",
                        "state": {},
                    },
                ],
            },
        ]
        text, tool_parts = OpencodeClient._parse_messages(messages)
        self.assertEqual(text, "")
        self.assertEqual(len(tool_parts), 2)
        self.assertEqual(tool_parts[0]["tool"], "read")
        self.assertEqual(tool_parts[1]["tool"], "write")


class TestOpencodeDbRead(unittest.TestCase):
    db: OpencodeDb

    @classmethod
    def setUpClass(cls):
        try:
            cls.db = OpencodeDb()
            # Verify we can read from the DB
            count = cls.db.get_message_count(cls.db.list_sessions(limit=1)[0]["id"])
        except Exception as e:
            raise SkipTest(f"Cannot read opencode DB: {e}")

    def test_list_sessions(self):
        sessions = self.db.list_sessions(limit=5)
        self.assertGreater(len(sessions), 0)
        for s in sessions:
            self.assertIn("id", s)
            self.assertIn("title", s)
            self.assertIn("directory", s)

    def test_get_session_messages(self):
        sessions = self.db.list_sessions(limit=3)
        for s in sessions:
            msgs = self.db.get_messages(s["id"])
            if msgs:
                for msg in msgs:
                    self.assertIn("info", msg)
                    self.assertIn("parts", msg)
                    self.assertIn("role", msg["info"])
                break

    def test_has_assistant_messages(self):
        sessions = self.db.list_sessions(limit=3)
        for s in sessions:
            if self.db.has_assistant_messages(s["id"]):
                self.assertTrue(self.db.has_data(s["id"]))
                return
        self.skipTest("no session with assistant messages found")


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

    def test_execute_task_returns_session_id(self):
        s = self.client.create_session(title="ut_exec")
        session_id = self.client.execute_task(s.id, "say hello")
        self.assertIsInstance(session_id, str)
        self.assertEqual(session_id, s.id)

    def test_wait_result(self):
        s = self.client.create_session(title="ut_wait")
        self.client.execute_task(s.id, "say hello")
        result = self.client.wait_result(s.id, timeout=120)
        self.assertIsInstance(result, Node)
        self.assertTrue(result.ok)
        self.assertIsInstance(result.get_value(), str)
        self.assertGreater(len(result.get_value()), 0)

    def test_wait_result_with_custom_wait_call(self):
        s = self.client.create_session(title="ut_wait_call")
        self.client.execute_task(s.id, "say hello")
        db = OpencodeDb.get_instance()
        result = self.client.wait_result(s.id, timeout=120, wait_call=db.is_session_complete)
        self.assertTrue(result.ok)

    def test_create_and_execute(self):
        s = self.client.create_session(title="ut_create_exec")
        self.client.execute_task(s.id, "say hi")
        result = self.client.wait_result(s.id, timeout=120)
        self.assertTrue(result.ok)

    def test_opencodedb_read(self):
        s = self.client.create_session(title="ut_db_read")
        self.client.execute_task(s.id, "say hello")
        result = self.client.wait_result(s.id, timeout=120)
        self.assertTrue(result.ok)
        db = OpencodeDb.get_instance()
        messages = db.get_messages(s.id)
        self.assertGreater(len(messages), 0)
        for msg in messages:
            self.assertIn("info", msg)
            self.assertIn("parts", msg)
            self.assertIn("role", msg["info"])


if __name__ == "__main__":
    unittest.main()
