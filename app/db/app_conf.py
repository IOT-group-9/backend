from pathlib import Path

from piccolo.conf.apps import AppConfig, table_finder

CURRENT_DIRECTORY = Path(__file__).parent

APP_CONFIG = AppConfig(
    app_name="app_db",
    migrations_folder_path=str(CURRENT_DIRECTORY / "migrations"),
    table_classes=[ 
        *table_finder(modules=["app.db.models.models"]),
    ],
    migration_dependencies=[],
    commands=[],
)
