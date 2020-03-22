#!/bin/sh
old_pid=$(ps -eo "pid,command" | grep tohru.py | grep -v grep | awk '{ print $1 }')
# awk '{ print $1 }' Prints first word from each line
if [[ -n $old_pid ]]; then
    echo "OLD PID "
    echo $old_pid
    echo "Restarting bot"
    kill -TERM $old_pid
    while ps -p $old_pid > /dev/null; do
        sleep 1
    done
else
    echo "Bot not running, starting up bot"
fi

python3 tohru.py > logs/bot.out 2>&1 & # 2 -Stderr, 1 - stdout. 2>&1 redirects stderr to stdout. & runs in bg.
echo "Waiting 5 second to make sure bot is up"
new_pid=$!
sleep 5
ps -ef | grep -v grep | grep $new_pid > /dev/null
if [ $? -eq 0 ] ; then # -eq (equals), 0 = found processor ID/grep succeeded, $? gets return code
    echo "Bot is now running"
else
    echo "Error starting up bot"
    cat logs/bot.out
fi
