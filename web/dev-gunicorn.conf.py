# Dev-Dla Gunicorn Conf

# Server socket

bind = "unix:dev-dla.sock"
backlog = 2048

# Worker processes

workers = 3
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Spew

spew = False

# Server mechanics

daemon = False
raw_env = [
    'VCONF=/home/dlink/dla/conf/dev.yaml',
    'PARAMETER_FILES_DIR=/home/dlink/dla/vreports']
pidfile = None
umask = 0
user = 'dlink'
group = 'dev'
tmp_upload_dir = None

# Logging

errorlog = '/var/log/gunicorn/dev-dla/error.log'
loglevel = 'debug'
accesslog = '/var/log/gunicorn/dev-dla/access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming

proc_name = 'gunicorn-dev-dla'

# Server hooks

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    ## get traceback info
    import threading, sys, traceback
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in list(sys._current_frames().items()):
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))

def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
