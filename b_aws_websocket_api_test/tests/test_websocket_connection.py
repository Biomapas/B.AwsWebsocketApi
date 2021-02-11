import asyncio
import json
import logging
import time
import websockets

from b_aws_websocket_api_test.infrastructure import Infrastructure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_websocket_connection() -> None:
    """
    Establishes a websocket connection with an API.
    Tries to send and receive a frame.

    :return: No return.
    """
    websocket_url = Infrastructure.get_output(Infrastructure.WEBSOCKET_API_URL_KEY)

    logger.info(f'Creating websocket connection with url: {websocket_url}.')

    async def hello(current_attempt: int = 0, max_attempts: int = 5, sleep_seconds: int = 10):
        if current_attempt == max_attempts:
            raise RecursionError()

        try:
            timeouts = dict(
                close_timeout=100,
                ping_timeout=100
            )

            async with websockets.connect(websocket_url, **timeouts) as websocket:
                await websocket.send(json.dumps(dict(action='test')))

                data = await websocket.recv()
                logger.info(f'Received data: {data}.')

                assert json.loads(data)['message'] == 'success'
        except websockets.exceptions.InvalidStatusCode as ex:
            logger.error(f'Status code from WS API: {ex}. Retrying...')

            time.sleep(sleep_seconds)

            current_attempt += 1

            await hello(current_attempt, max_attempts, sleep_seconds)

    asyncio.get_event_loop().run_until_complete(hello())
