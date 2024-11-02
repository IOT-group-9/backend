from fastapi.routing import APIRouter, Mount
from piccolo.apps.user.tables import BaseUser
from piccolo.conf.apps import table_finder
from piccolo_admin.endpoints import create_admin

from app.web.api import (
    docs,  
    echo, 
    monitoring, 
    rabbit, 
    redis, 
    sensor,
    parking,
    display,
    test
)

api_router = APIRouter()

# Existing routes
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(rabbit.router, prefix="/rabbit", tags=["rabbit"])
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
api_router.include_router(sensor.sensor_router, prefix="/sensor", tags=["sensor"])

# New routes
api_router.include_router(parking.parking_router, prefix="/parking", tags=["parking"])
api_router.include_router(display.display_router, prefix="/display", tags=["display"])
api_router.include_router(test.test_router, prefix="/test", tags=["test"])

# Admin route
admin_route = Mount(
    path="/admin/",
    app=create_admin(
        tables=[*table_finder(modules=["app.db.models.models"]), BaseUser],
        # Specify a different site name in the
        # admin UI (default Piccolo Admin):
        site_name="My Site Admin",
        # Required when running under HTTPS:
        # ERA001 allowed_hosts=["my_site.com"],
    ),
)
