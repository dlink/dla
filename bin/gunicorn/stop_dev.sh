# This script stops the dev gunicorn daemon

# look for
PROG='dev-gunicorn.conf.py'

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
    echo Error: $PROG not running
    exit 1
fi

# kill them
kill -9 $pids

# report success or fail
if [ $? -ne 0 ]; then
    echo "Failed to stop $PROG"
else
    echo "$PROG Successfully stopped"
fi
