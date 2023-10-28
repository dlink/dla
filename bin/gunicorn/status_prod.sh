# This script stops the dev gunicorn daemon

# look for
#PROG='gunicorn.conf.py'
PROG='/data/apps/dla/.venv/bin/gunicorn'

# cmd to find process
cmd="ps -ef | grep $PROG | grep -v -e grep -e tail"

# cmd to get their pids
cmd2="$cmd | awk '{print \$2}'"

# show processes
#eval $cmd

# get pids
pids=`eval $cmd2`

# check if we have pids
if [ -z "$pids" ] ; then
    echo "$PROG is not running"
else
    echo "$PROG is running"
fi
