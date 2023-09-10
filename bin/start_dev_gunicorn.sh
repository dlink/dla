# This script starts up the dev gunicorn daemon

cd ~/dla
source .venv/bin/activate
cd web
export PYTHONPATH='/home/dlink/dla/lib:/home/dlink/dla/web:/home/dlink/vweb/src:/home/dlink/vlib/src'
gunicorn --daemon --reload -c dev-gunicorn.conf.py wsgi:app
