# This script starts up the prod gunicorn daemon

cd /apps/dla
source .venv/bin/activate
cd web
export PYTHONPATH='/apps/dla/lib:/apps/dla/web:/apps/vweb/src:/apps/vlib/src'

# app:app = module_name:variable
# this runs web/apps.py: app().run()
gunicorn --daemon --reload -c gunicorn.conf.py app:app
