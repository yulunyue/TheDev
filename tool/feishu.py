"""
飞书 CLI 工具
用法：
    python -m tool.feishu auth                           # OAuth 登录
    python -m tool.feishu read [wiki_token]               # 读取文档/sheet
    python -m tool.feishu write [wiki_token] [--range A1:B2] [--values ...]  # 写入
    python -m tool.feishu upload <file> [--cell A1]      # 上传文件到表格
    python -m tool.feishu img <image> [--cell A1]        # 插入图片到单元格
"""

import argparse
import json
import os

from common.third_util.feishu import login, get_valid_user_token, resolve_node
from common.third_util.feishu.sheet import read_range, write_range, spreadsheet_meta, insert_image
from common.third_util.feishu.drive import upload_media, make_attachment

DEFAULT_WIKI = "Szwrwgy6siVYKvksfPWc0g7ynGd"
DEFAULT_SHEET = "6cba43"
REDIRECT_PORT = 51497


def cmd_auth(args):
    login(REDIRECT_PORT)


def cmd_read(args):
    wiki = args.wiki_token or DEFAULT_WIKI
    user_token = get_valid_user_token()

    print(f"解析 wiki 节点: {wiki}")
    obj_token, obj_type, title = resolve_node(wiki, user_token)
    print(f"  type={obj_type}  title={title}  token={obj_token}")

    if obj_type == "sheet":
        print(f"\n读取工作表 {DEFAULT_SHEET}...")
        meta = spreadsheet_meta(obj_token, user_token)
        print(f"  元信息: {json.dumps(meta, ensure_ascii=False, indent=2)[:500]}")

        data = read_range(obj_token, DEFAULT_SHEET, user_token=user_token)
        print(f"\n数据（{len(data)} 行）:")
        for i, row in enumerate(data[:30]):
            print(f"  [{i}] {row}")

    elif obj_type in ("docx", "doc"):
        from common.third_util.feishu.doc import read_raw_content

        content = read_raw_content(obj_token, user_token)
        print(f"\n文档内容（前 1000 字）:")
        print(content[:1000])

    else:
        print(f"暂不支持处理 type={obj_type} 的内容")


def cmd_write(args):
    wiki = args.wiki_token or DEFAULT_WIKI
    user_token = get_valid_user_token()

    obj_token, obj_type, title = resolve_node(wiki, user_token)
    if obj_type != "sheet":
        print(f"错误：该文档类型为 {obj_type}，不是电子表格")
        return

    sheet_id = args.sheet_id or DEFAULT_SHEET
    range_ = args.range or "A1:B2"
    values = json.loads(args.values)

    print(f"写入 {obj_token}/{sheet_id}!{range_}: {values}")
    rev = write_range(obj_token, sheet_id, range_, values, user_token)
    print(f"成功，revision={rev}")


def cmd_upload(args):
    wiki = args.wiki_token or DEFAULT_WIKI
    user_token = get_valid_user_token()

    obj_token, obj_type, title = resolve_node(wiki, user_token)
    if obj_type != "sheet":
        print(f"错误：该文档类型为 {obj_type}，不是电子表格")
        return

    file_path = args.file
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return

    sheet_id = args.sheet_id or DEFAULT_SHEET
    print(f"上传文件到电子表格: {file_path}")
    file_token = upload_media(file_path, obj_token, parent_type="sheet_file", extra={"drive_route_token": obj_token}, user_token=user_token)
    print(f"上传成功，file_token={file_token}")

    cell = args.cell or "B1"
    att = make_attachment(file_token, os.path.basename(file_path))
    rev = write_range(obj_token, sheet_id, cell, [att], user_token)
    print(f"写入单元格 {cell} 成功，revision={rev}")


def cmd_img(args):
    wiki = args.wiki_token or DEFAULT_WIKI
    user_token = get_valid_user_token()

    obj_token, obj_type, title = resolve_node(wiki, user_token)
    if obj_type != "sheet":
        print(f"错误：该文档类型为 {obj_type}，不是电子表格")
        return

    image_path = args.image
    if not os.path.exists(image_path):
        print(f"文件不存在: {image_path}")
        return

    sheet_id = args.sheet_id or DEFAULT_SHEET
    cell = args.cell or "A1"
    print(f"插入图片到 {obj_token}/{sheet_id}!{cell}: {image_path}")
    rev = insert_image(obj_token, sheet_id, cell, image_path, user_token=user_token)
    print(f"成功，revision={rev}")


def main():
    parser = argparse.ArgumentParser(description="飞书 CLI 工具")
    sub = parser.add_subparsers(dest="cmd")

    p_auth = sub.add_parser("auth", help="OAuth 登录")

    p_read = sub.add_parser("read", help="读取文档/表格")
    p_read.add_argument("wiki_token", nargs="?", default=None)

    p_write = sub.add_parser("write", help="写入电子表格")
    p_write.add_argument("wiki_token", nargs="?", default=None)
    p_write.add_argument("--sheet-id", default=DEFAULT_SHEET)
    p_write.add_argument("--range", default="A1:B2")
    p_write.add_argument("--values", required=True, help='JSON 数组')

    p_upload = sub.add_parser("upload", help="上传文件到表格单元格")
    p_upload.add_argument("wiki_token", nargs="?", default=None)
    p_upload.add_argument("file", help="本地文件路径")
    p_upload.add_argument("--sheet-id", default=DEFAULT_SHEET)
    p_upload.add_argument("--cell", default="B1", help="目标单元格，如 B1")

    p_img = sub.add_parser("img", help="插入图片到单元格")
    p_img.add_argument("wiki_token", nargs="?", default=None)
    p_img.add_argument("image", help="本地图片路径")
    p_img.add_argument("--sheet-id", default=DEFAULT_SHEET)
    p_img.add_argument("--cell", default="A1", help="目标单元格，如 A1")

    args = parser.parse_args()
    if args.cmd == "auth":
        cmd_auth(args)
    elif args.cmd == "read":
        cmd_read(args)
    elif args.cmd == "write":
        cmd_write(args)
    elif args.cmd == "upload":
        cmd_upload(args)
    elif args.cmd == "img":
        cmd_img(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
