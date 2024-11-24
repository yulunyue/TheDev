#PID=$(ps -ef | grep 'python3 /opt/cloud/thedev/main.py run' | head -n 1 | awk '{ print $2}')
PID=$(netstat -nltp | grep 8888 | awk -F/ '{print $1}' | awk '{print $7}')
echo MAIN PID $PID
kill -9 $PID
python3 /opt/cloud/thedev/main.py run >/opt/cloud/thedev/data/log/run.log 2>&1 &