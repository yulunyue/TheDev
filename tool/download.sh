REMOTE="root@1.14.97.154"
REMOTE_DIR="/root/TheDev"

if [ -z "$1" ]; then
    echo "用法: $0 <远程路径> [本地目标路径]"
    echo "示例:"
    echo "  $0 config/setting/todo_category.json"
    echo "  $0 data/log/run.log data/tmp/run.log"
    exit 1
fi

REMOTE_PATH="$1"
LOCAL_DEST="${2:-$REMOTE_PATH}"
mkdir -p "$(dirname "$LOCAL_DEST")"
echo "下载 $REMOTE:$REMOTE_DIR/$REMOTE_PATH 到 $LOCAL_DEST"
scp -r "$REMOTE:$REMOTE_DIR/$REMOTE_PATH" "$LOCAL_DEST"
