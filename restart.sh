PID=$(ps -ef | grep 'python3 /opt/cloud/thedev/main.py run' | head -n 1 | awk '{ print $2}')
echo MAIN PID $PID
kill -9 $PID
python3 /opt/cloud/thedev/main.py run & >/dev/null 2>&1