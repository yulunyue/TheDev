NAME=$1
PROCESS_NAME="main.py ${NAME}"
TASK_INFO=$(ps aux | grep -F "$PROCESS_NAME" | grep -v grep | grep -v "$0")
echo ${TASK_INFO}
PID=$(echo "$TASK_INFO" | awk '{print $2}')
echo PID:$PID
kill -9 $PID
nohup python3 main.py $NAME 2>&1 &