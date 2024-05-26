import logging
import threading

import socketio
import arena
import time
from aiohttp import web
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import BasicAuth

MAX_NUMBER_OF_PLAYER = 10

# -------------------------------------------------------------------

async def index(request, arena):
    if arena.getNumberOfPlayers() >= MAX_NUMBER_OF_PLAYER:
        return web.Response(status=503, text="Too many players in the server, please try again in a few moments")
    else:
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
    while True:
        await updateArena(sio, namespace, arena)
        await asyncio.sleep(1)

async def updateArena(sio, namespace, arena):
    arena.update(time.time())
    await sio.emit('updates', data=arena.toJSON(), skip_sid=True, namespace=namespace)

async def shutdown(sio, namespace):
    await sio.emit('issues', data={'message': "shutdown"}, skip_sid=True, namespace=namespace)
    pass

async def healthCheck(arena):
    playerCount = arena.getNumberOfPlayers()
    status = 200 if playerCount < MAX_NUMBER_OF_PLAYER else 500
    print("Health check: " + str(playerCount) + " players")
    return web.Response(status=status, text=str(playerCount))


# -------------------------------------------------------------------

def initSocketIO(app, namespace):
    sio = socketio.AsyncServer(async_mode='aiohttp')
    sio.attach(app)

    @sio.on('connect', namespace=namespace)
    def connect(sid, data):
        print("connect", sid)

    @sio.on('disconnect', namespace=namespace)
    async def disconnect(sid):
        print("disconnect", sid)
        await disconnect_command(sid, app['arena'])

    @sio.on('command', namespace=namespace)
    async def command(sid, data):
        if data['command'] == "connect" and app['arena'].getNumberOfPlayers() >= MAX_NUMBER_OF_PLAYER:
            await sio.emit('issues', data={"message": "reload"}, skip_sid=True, namespace=namespace, room=sid)
            return
        await globals()[data['command'] + '_command'](sid, app['arena'], data)
        await updateArena(sio, namespace, app['arena'])

    return sio

async def auth_middleware(app, handler):
    async def middleware_handler(request):
        if request.path == '/':
            auth = request.headers.get('Authorization')
            if auth is None:
                return web.Response(status=401, headers={'WWW-Authenticate': 'Basic realm="SnAkE"'})
            try:
                username, password = BasicAuth.decode(auth)
                if username != 'admin' or password != 'password':
                    return web.Response(status=403, text='Forbidden')
            except ValueError:
                return web.Response(status=400, text='Bad Request')
        return await handler(request)
    return middleware_handler

# -------------------------------------------------------------------

def between_callback(app, namespace):
    loop = asyncio.new_event_loop()
    updateTask = loop.create_task(periodicUpdateArena(app['socketIO'], namespace, app['arena']))

    loop.run_until_complete(updateTask)
    loop.close()

def main():
    logging.basicConfig(level=logging.ERROR)
    namespace = '/snake'

    app = web.Application(middlewares=[auth_middleware])

    app['arena'] = arena.Arena(time.time())

    app.router.add_get('/',            lambda request: index(request, app['arena']))
    app.router.add_get('/healthCheck', lambda request: healthCheck(app['arena']))
    app.router.add_static('/js',  '../client/js')
    app.router.add_static('/css', '../client/css')

    app['socketIO'] = initSocketIO(app, namespace)
    app.on_shutdown.append(lambda value: shutdown(app['socketIO'], namespace))

    _thread = threading.Thread(target=between_callback, args=(app, namespace))
    _thread.start()

    web.run_app(app)


if __name__ == '__main__':
    main()
