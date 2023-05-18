import logging
import secrets

import socketio
import arena
import time
from aiohttp import web
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

MAX_NUMBER_OF_PLAYER = 2

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
    arena.update(time.time())
    await sio.emit('updates', data=arena.toJSON(), skip_sid=True, namespace=namespace)
    print("sent automatic update")
    await asyncio.sleep(0.1)
    loop = asyncio.get_event_loop()
    loop.create_task(periodicUpdateArena(sio, namespace, arena))

async def updateArena(sio, namespace, arena):
    arena.update(time.time())
    await sio.emit('updates', data=arena.toJSON(), skip_sid=True, namespace=namespace)


async def shutdown(sio, namespace):
    await sio.emit('issues', data={'message': "shutdown"}, skip_sid=True, namespace=namespace)
    pass

async def healthCheck(arena):
    MAX_PLAYERS = 5
    playerCount = arena.getNumberOfPlayers()
    status = 200 if playerCount < MAX_PLAYERS else 500
    print("Health check: " + str(playerCount) + " players")
    return web.Response(status=status, text=str(playerCount))


# -------------------------------------------------------------------

def initSocketIO(app, namespace):
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
        if data['command'] == "connect" and app['arena'].getNumberOfPlayers() >= MAX_NUMBER_OF_PLAYER:
            print("Too many players while page already loaded")
            await sio.emit('issues', data={"message": "reload"}, skip_sid=True, namespace=namespace, room=sid)
            return
        await globals()[data['command'] + '_command'](sid, app['arena'], data)
        await updateArena(sio, namespace, app['arena'])

    return sio


# -------------------------------------------------------------------

def main():
    logging.basicConfig(level=logging.ERROR)
    namespace = '/snake'

    app = web.Application()

    app['arena'] = arena.Arena(time.time())

    app.router.add_get('/', lambda request: index(request, app['arena']))
    app.router.add_get('/healthCheck', lambda request: healthCheck(app['arena']))
    app.router.add_static('/js', '../client/js')
    app.router.add_static('/css', '../client/css')

    app['socketIO'] = initSocketIO(app, namespace)
    app.on_shutdown.append(lambda value: shutdown(app['socketIO'], namespace))

    loop = asyncio.get_event_loop()
    loop.create_task(periodicUpdateArena(app['socketIO'], namespace, app['arena']))
    web.run_app(app)


if __name__ == '__main__':
    main()