from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine
from piccolo.engine.sqlite import SQLiteEngine

from app.settings import settings

DB: PostgresEngine | SQLiteEngine
if settings.enable_sqlite:
    DB = SQLiteEngine(path=settings.root_directory / "piccolo.sqlite")
else:
    DB = PostgresEngine(
        config={
            "database": settings.db_base,
            "user": settings.db_user,
            "password": settings.db_pass,
            "host": settings.db_host,
            "port": settings.db_port,
        },
    )


APP_REGISTRY = AppRegistry(
    apps=[
        "app.db.app_conf",
        "piccolo_admin.piccolo_app",
        "piccolo.apps.user.piccolo_app",
        "piccolo_api.session_auth.piccolo_app",
    ],
)
