import asyncio
import json
import socket
from datetime import datetime, timezone

import websockets


async def listen_forever(url, subscribe_func, parse_func):
    while True:
        try:
            async with websockets.connect(url) as ws:
                await subscribe_func(ws)
                while True:
                    try:
                        data = await asyncio.wait_for(ws.recv(), timeout=None)
                    except (asyncio.TimeoutError, websockets.ConnectionClosed):
                        pong = await ws.ping()
                        await asyncio.wait_for(pong, timeout=10)
                        continue
                    except:
                        await asyncio.sleep(10)
                        break

                    parse_func(json.loads(data))

        except socket.gaierror:
            continue
        except KeyboardInterrupt:
            break


def get_timestamp():
    return datetime.now(timezone.utc).isoformat()


def parse_bitflyer_timestamp(ts: str):
    ts = ts[: -max(len(ts) - 26, 1)]  # ミリ秒の桁を揃える
    return f"{ts:<026}+00:00"
