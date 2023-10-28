# This script starts up the dev gunicorn daemon

PROG='dev-gunicorn.conf.py'

cd ~/dla
source .venv/bin/activate
cd web
export PYTHONPATH='/home/dlink/dla/lib:/home/dlink/dla/web:/home/dlink/vweb/src:/home/dlink/vlib/src'

# app:app = module_name:variable
# this runs web/apps.py: app().run()
gunicorn --daemon --reload -c dev-gunicorn.conf.py app:app

echo "$PROG successfully started"
