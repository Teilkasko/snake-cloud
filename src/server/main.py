import logging
import socketio
import sched, time
import arena
from aiohttp import web

async def index(request):
    return web.FileResponse('../client/index.html')

# -------------------------------------------------------------------

def connect_command (arena, data):
    print("CONNECT COMMAND", arena, data)

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
        print("connect", sid)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        print("disconnect", sid)
        # await sio.disconnect(sid, namespace='/snake')

    @sio.on('updates', namespace=namespace)
    async def message(sid, data):
        """Get message from client and reply with same message to it."""
        #   print("updates", data, sid)
        await sio.emit('updates', data=data, skip_sid=True, namespace=namespace)

    @sio.on('command', namespace=namespace)
    def my_event(sid, data):
        globals()[data['command'] + '_command'](app['arena'], data)

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
