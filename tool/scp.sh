REMOTE="root@1.14.97.154"
REMOTE_DIR="/root/TheDev"

if [ "$1" == "-d" ] || [ "$1" == "--download" ]; then
    REMOTE_PATH="$2"
    LOCAL_DEST="${3:-$REMOTE_PATH}"
    mkdir -p "$(dirname "$LOCAL_DEST")"
    echo "下载 $REMOTE:$REMOTE_DIR/$REMOTE_PATH 到 $LOCAL_DEST"
    scp -r "$REMOTE:$REMOTE_DIR/$REMOTE_PATH" "$LOCAL_DEST"

elif [ -n "$1" ]; then
    LOCAL_PATH="$1"
    if [ -d "$LOCAL_PATH" ]; then
        echo "$LOCAL_PATH 是目录"
        scp -r "$LOCAL_PATH" "$REMOTE:$REMOTE_DIR/$LOCAL_PATH"
    elif [ -f "$LOCAL_PATH" ]; then
        echo "$LOCAL_PATH 是普通文件"
        scp "$LOCAL_PATH" "$REMOTE:$REMOTE_DIR/$LOCAL_PATH"
    else
        echo "$LOCAL_PATH 不存在或不是文件/目录"
        exit 1
    fi
else
    echo "用法:"
    echo "  上传: $0 <本地路径>"
    echo "  下载: $0 -d <远程路径> [本地目标路径]"
    exit 1
fi