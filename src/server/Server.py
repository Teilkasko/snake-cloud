# Web Application that will handle websocket, with write received by Main.py calls, and values pushed to all web clients

import logging
import socketio
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

# -------------------------------------------------------------------

def main():
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_static('/js', '../client/js')

    sio.attach(app)
    app.on_shutdown.append(shutdown)

    web.run_app(app)


async def shutdown(app):
    pass


if __name__ == '__main__':
    main()
