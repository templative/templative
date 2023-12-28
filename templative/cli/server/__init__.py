from aiohttp import web
import aiohttp_cors
import asyncclick as click
from .httpRoutes import routes
from .socketRoutes import sio

@click.command()
@click.option('--port', default=8080, required=False, help='The port of the local server.')
async def serve(port):
    """Serve Templative as a socket and http server"""
    
    app = web.Application()
    app.add_routes(routes)
    sio.attach(app)
    aiohttp_cors.setup(app, defaults={
      "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*"
        )
      })

    await web._run_app(app, host="localhost", port=port)

