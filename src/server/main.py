import logging
import socketio
import sched, time
import arena
from aiohttp import web

sio = socketio.AsyncServer(async_mode='aiohttp')

async def index(request):
    return web.FileResponse('../client/index.html')

# -------------------------------------------------------------------

@sio.on('connect', namespace='/snake')
def connect(sid, environ):
    """On connection event from client print to stdout the connect event and sid of client."""
    print("connect ", sid)

@sio.on('disconnect', namespace='/snake')
async def disconnect(sid):
    """Close socket connection for client with specified sid."""
    print('disconnect ', sid)
    #await sio.disconnect(sid, namespace='/snake')

@sio.on('updates', namespace='/snake')
async def message(sid, data):
    """Get message from client and reply with same message to it."""
#   print("updates", data, sid)
    await sio.emit('updates', data=data, skip_sid=True, namespace='/snake')

@sio.on('command', namespace='/snake')
def my_event(sid, data):
    """Get message from client and print to stdout."""
    print("command", sid, data)
    command = data['command']


# -------------------------------------------------------------------

def connect_command (data):
    print("CONNECT COMMAND", data)

# -------------------------------------------------------------------
'''
def start_background_scheduler ():
    scheduler = sched.scheduler(time.time, time.sleep)
    def do_something(sc):
        print("Doing stuff...")
        # do your stuff
        scheduler.enter(60, 1, do_something, (sc,))

    scheduler.enter(60, 1, do_something, (scheduler,))
    scheduler.run()
'''

async def shutdown(app):
    pass

# -------------------------------------------------------------------

def main():
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_static('/js', '../client/js')

    app['arena'] = arena.Arena()
    sio.attach(app)
    app.on_shutdown.append(shutdown)

    #start_background_scheduler()
    web.run_app(app)


if __name__ == '__main__':
    main()
