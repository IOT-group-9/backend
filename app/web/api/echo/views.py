from fastapi import APIRouter

from app.web.api.echo.schema import Message
from app.tkq import broker
from httpx import AsyncClient
from app.settings import settings
router = APIRouter()


@router.post("/", response_model=Message)
async def send_echo_message(
    incoming_message: Message,
) -> Message:
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """
    return incoming_message

@router.get("/taskiq")
async def send_publish():
    task = await send_publish_request.kiq()
    # Wait for the result.
    result = await task.wait_result(timeout=30)
    print(f"Task execution took: {result.execution_time} seconds.")
    if not result.is_err:
        print(f"Returned value: {result.return_value}")
    else:
        print("Error found while executing task.")

@broker.task
async def add_one(value: int) -> int:
    return value + 1

@broker.task
async def send_publish_request():
    async with AsyncClient() as client:
        await client.get(f"{settings.listening_url}/api/pubsub/publish/1/1")
    return "done!"
