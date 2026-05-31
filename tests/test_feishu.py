import pytest

from common.third_util.feishu.client import FeishuClient
from common.third_util.feishu.auth import get_valid_user_token
from common.third_util.feishu.wiki import resolve_node
from common.third_util.feishu.sheet import read_range, write_range, spreadsheet_meta, insert_image
from common.third_util.feishu.doc import read_raw_content
from common.third_util.feishu.drive import upload_file, upload_media, make_attachment

WIKI_TOKEN = "Szwrwgy6siVYKvksfPWc0g7ynGd"
SHEET_ID = "6cba43"


class TestFeishuClient:
    def test_singleton(self):
        c1 = FeishuClient.get()
        c2 = FeishuClient.get()
        assert c1 is c2

    def test_client_has_attr(self):
        c = FeishuClient.get()
        assert hasattr(c, "client")
        assert hasattr(c, "app_id")


class TestApi:
    @pytest.mark.skip(reason="Requires Feishu API and valid auth")
    def test_resolve_node(self):
        user_token = get_valid_user_token()
        obj_token, obj_type, title = resolve_node(WIKI_TOKEN, user_token)
        assert obj_token
        assert obj_type
        assert title

    @pytest.mark.skip(reason="Requires Feishu API and valid auth")
    def test_read_sheet(self):
        user_token = get_valid_user_token()
        obj_token, obj_type, _ = resolve_node(WIKI_TOKEN, user_token)
        assert obj_type == "sheet"
        values = read_range(obj_token, SHEET_ID, user_token=user_token)
        assert isinstance(values, list)
        assert len(values) > 0

    @pytest.mark.skip(reason="Requires Feishu API and valid auth")
    def test_spreadsheet_meta(self):
        user_token = get_valid_user_token()
        obj_token, obj_type, _ = resolve_node(WIKI_TOKEN, user_token)
        meta = spreadsheet_meta(obj_token, user_token)
        assert "sheets" in meta

    @pytest.mark.skip(reason="Requires Feishu API and valid auth")
    def test_write_then_read(self):
        user_token = get_valid_user_token()
        obj_token, obj_type, _ = resolve_node(WIKI_TOKEN, user_token)
        test_values = [["test_write", "hello"]]
        rev = write_range(obj_token, SHEET_ID, "A1:B1", test_values, user_token)
        assert rev > 0
        values = read_range(obj_token, SHEET_ID, "A1:B1", user_token)
        assert values == test_values

    @pytest.mark.skip(reason="Requires Feishu API and valid auth")
    def test_read_doc(self):
        user_token = get_valid_user_token()
        content = read_raw_content("dummy", user_token)
        assert isinstance(content, str)


class TestDrive:
    def test_make_attachment(self):
        att = make_attachment("file_token_xxx", "test.zip")
        assert att[0]["type"] == "attachment"
        assert att[0]["fileToken"] == "file_token_xxx"
        assert att[0]["text"] == "test.zip"

    @pytest.mark.skip(reason="Requires Feishu API and valid auth")
    def test_upload_media(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"fake png content")
            tmp = f.name
        try:
            user_token = get_valid_user_token()
            obj_token, obj_type, _ = resolve_node(WIKI_TOKEN, user_token)
            file_token = upload_media(tmp, obj_token, parent_type="sheet_image", user_token=user_token)
            assert file_token
        finally:
            os.unlink(tmp)


class TestSheetImage:
    @pytest.mark.skip(reason="Requires Feishu API and valid auth")
    def test_insert_image(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"fake png content")
            tmp = f.name
        try:
            user_token = get_valid_user_token()
            obj_token, obj_type, _ = resolve_node(WIKI_TOKEN, user_token)
            rev = insert_image(obj_token, SHEET_ID, "Z1", tmp, user_token=user_token)
            assert rev > 0
        finally:
            os.unlink(tmp)
