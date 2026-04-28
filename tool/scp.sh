PATH=$1
REMOTE=root@1.14.97.154
if [ -d "$PATH" ]; then
    echo "$PATH 是目录"
    scp -r $PATH $REMOTE/$PATH/root/TheDev
elif [ -f "$PATH" ]; then
    echo "$PATH 是普通文件"
    scp $PATH $REMOTE/$PATH/root/TheDev
else
    echo "$PATH 不存在或不是文件/目录"
fi