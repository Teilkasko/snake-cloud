import logging
import socketio
import arena
import time
from aiohttp import web
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def index(request):
    return web.FileResponse('../client/index.html')

# -------------------------------------------------------------------

async def connect_command (sid, arena, data):
    arena.addUser(sid, data['username'])

async def snake_up_command(sid, arena, data):
    arena.changeSnakeDirection(sid, 'up', time.time())

async def snake_left_command(sid, arena, data):
    arena.changeSnakeDirection(sid, 'left', time.time())

async def snake_right_command(sid, arena, data):
    arena.changeSnakeDirection(sid, 'right', time.time())

async def snake_down_command(sid, arena, data):
    arena.changeSnakeDirection(sid, 'down', time.time())

async def disconnect_command (sid, arena):
    arena.removeUser(sid)

# -------------------------------------------------------------------

async def periodicUpdateArena(sio, namespace, arena):
    arena.update(time.time())
    await sio.emit('updates', data=arena.toJSON(), skip_sid=True, namespace=namespace)
    await asyncio.sleep(0.1)
    loop = asyncio.get_event_loop()
    loop.create_task(periodicUpdateArena(sio, namespace, arena))

async def updateArena(sio, namespace, arena):
    arena.update(time.time())
    await sio.emit('updates', data=arena.toJSON(), skip_sid=True, namespace=namespace)


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
        await disconnect_command(sid, app['arena'])

    @sio.on('command', namespace=namespace)
    async def command(sid, data):
        await globals()[data['command'] + '_command'](sid, app['arena'], data)
        await updateArena(sio, namespace, app['arena'])

    return sio

# -------------------------------------------------------------------

def main():
    logging.basicConfig(level=logging.ERROR)
    namespace = '/snake'

    routes = web.RouteTableDef()

    @routes.get('/healthCheck')
    async def healthCheck(request):
        MAX_PLAYERS = 5
        playerCount = app['arena'].getNumberOfPlayers()
        status = 200 if playerCount < MAX_PLAYERS else 500
        print("Health check: " + str(playerCount) + " players")
        return web.Response(status=status, text=str(playerCount))

    app = web.Application()

    app['arena'] = arena.Arena(time.time())

    app.router.add_get('/', index)
    app.router.get('/healthCheck', lambda request: healthCheck(app['arena']))
    app.router.add_static('/js', '../client/js')
    app.router.add_static('/css', '../client/css')
    app.add_routes(routes)

    app['socketIO'] = initSocketIO(app, namespace)
    app.on_shutdown.append(shutdown)

    '''sched = AsyncIOScheduler()
    sched.add_job(_updateArena(app['socketIO'], namespace, app['arena']), 'interval', seconds = 0.1)
    sched.start()'''
    loop = asyncio.get_event_loop()
    loop.create_task(periodicUpdateArena(app['socketIO'], namespace, app['arena']))
    web.run_app(app)


if __name__ == '__main__':
    main()
