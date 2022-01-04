from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles

from ..conf import settings
from .categories import categories_route
from .category import category_route
from .error_500 import error_500_route
from .hooks import register_routes_hook
from .index import index_route
from .thread import thread_route
from .threads import threads_route
from .exceptions import HTTPNotFound, get_exception_handlers


def register_routes(app: Starlette):
    register_routes_hook.call_action(register_default_routes, app)


def register_default_routes(app: Starlette):
    app.add_route("/", index_route, name="index")
    app.add_route("/categories/", categories_route, name="categories")
    app.add_route("/threads/", threads_route, name="threads")
    app.add_route("/c/{slug}/{id:int}/", category_route, name="category")
    app.add_route("/t/{slug}/{id:int}/", thread_route, name="thread")
    app.add_route("/t/{slug}/{id:int}/{page:int}/", thread_route, name="thread")

    if settings.debug:
        app.mount("/static/", StaticFiles(directory=settings.static_root))
        app.mount("/media/", StaticFiles(directory=settings.media_root))
        app.add_route("/error-500/", error_500_route, include_in_schema=False)