# This script activates the dev-dla python virtual environment
# And sets PYTHONPATH and VCONF env variables for the command line
# It is generally called from $HOME/.profile
#
#   Usage:
#      source bin/set_dev_env.sh

# deactivate virtual_env if nec
if [[ ! -z "$VIRTUAL_ENV" ]] ; then
    deactivate
fi

# activate
cd $HOME/dla
source .venv/bin/activate

# dev env
source $HOME/dla/bin/aliases
export PYTHONPATH=$HOME/dla/lib:$HOME/vlib/src:$HOME/vweb/src
export VCONF=$HOME/dla/conf/dev.yaml
PATH=$PATH:$HOME/dla/bin:$HOME/dla/lib
