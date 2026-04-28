LOCAL_PATH="$1"
REMOTE="root@1.14.97.154"
REMOTE_DIR="/root/TheDev"

# 确保远程目录存在（可选但推荐）
# $ssh "$REMOTE" "mkdir -p $REMOTE_DIR"

if [ -d "$LOCAL_PATH" ]; then
    echo "$LOCAL_PATH 是目录"
    scp -r "$LOCAL_PATH" "$REMOTE:$REMOTE_DIR/"
elif [ -f "$LOCAL_PATH" ]; then
    echo "$LOCAL_PATH 是普通文件"
    scp "$LOCAL_PATH" "$REMOTE:$REMOTE_DIR/"
else
    echo "$LOCAL_PATH 不存在或不是文件/目录"
    exit 1
fi