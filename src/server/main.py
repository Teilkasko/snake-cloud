import logging
import socketio
import sched, time
import arena
from aiohttp import web

async def index(request):
    return web.FileResponse('../client/index.html')

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

def initSocketIO (app):
    namespace = '/snake'
    sio = socketio.AsyncServer(async_mode='aiohttp')
    sio.attach(app)

    @sio.on('connect', namespace=namespace)
    def connect(sid, environ):
        """On connection event from client print to stdout the connect event and sid of client."""
        print("connect", sid)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        """Close socket connection for client with specified sid."""
        print("disconnect", sid)
        # await sio.disconnect(sid, namespace='/snake')

    @sio.on('updates', namespace=namespace)
    async def message(sid, data):
        """Get message from client and reply with same message to it."""
        #   print("updates", data, sid)
        await sio.emit('updates', data=data, skip_sid=True, namespace=namespace)

    @sio.on('command', namespace=namespace)
    def my_event(sid, data):
        """Get message from client and print to stdout."""
        print("command", sid, data, app['arena'])
        command = data['command']

    return sio

# -------------------------------------------------------------------

def main():
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_static('/js', '../client/js')

    app['arena'] = arena.Arena()
    app['socketIO'] = initSocketIO(app)
    app.on_shutdown.append(shutdown)

    #start_background_scheduler()
    web.run_app(app)


if __name__ == '__main__':
    main()
