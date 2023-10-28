# This script activates the prod dla python virtual environment
# And sets PYTHONPATH and VCONF env variables for the command line
# It is generally called from bin/gunicorn/start_prod.sh
#
#   Usage:
#      source bin/set_prod_env

# deactivate virtual_env if nec
if [[ ! -z "$VIRTUAL_ENV" ]] ; then
    deactivate
fi

# activate
cd /apps/dla
source .venv/bin/activate

# dev env
source /apps/dla/bin/aliases
export PYTHONPATH=/apps/dla/lib:/apps/vlib/src:/apps/vweb/src
export VCONF=/apps/dla/conf/prod.yaml
