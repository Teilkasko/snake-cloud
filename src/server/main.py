import logging
import socketio
import arena
import time
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def index(request):
    return web.FileResponse('../client/index.html')

# -------------------------------------------------------------------

async def connect_command (sid, arena, data):
    arena.addUser(sid, data['username'])

# -------------------------------------------------------------------

def updateArena(sio, namespace, arena):
    async def _updateArena():
        arena.update(time.time())
        await sio.emit('updates', data=arena.toJSON(), skip_sid=True, namespace=namespace)
    
    return _updateArena

async def shutdown(app):
    pass

# -------------------------------------------------------------------

def initSocketIO (app, namespace):
    sio = socketio.AsyncServer(async_mode='aiohttp')
    sio.attach(app)

    @sio.on('connect', namespace=namespace)
    def connect(sid, environ):
        print("connect", sid)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        print("disconnect", sid)

    @sio.on('command', namespace=namespace)
    async def command(sid, data):
        await globals()[data['command'] + '_command'](sid, app['arena'], data)
        #await updateArena(sio, namespace, arena)

    return sio

# -------------------------------------------------------------------

def main():
    logging.basicConfig(level=logging.ERROR)
    namespace = '/snake'

    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_static('/js', '../client/js')

    app['arena'] = arena.Arena(time.time())
    app['socketIO'] = initSocketIO(app, namespace)
    app.on_shutdown.append(shutdown)

    sched = AsyncIOScheduler()
    sched.add_job(updateArena(app['socketIO'], namespace, app['arena']), 'interval', seconds = 5)
    sched.start()
    web.run_app(app)


if __name__ == '__main__':
    main()
