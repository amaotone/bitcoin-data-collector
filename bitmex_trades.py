import asyncio
import json

from collector import get_timestamp, listen_forever


def parse(data):
    now = get_timestamp()
    if not (data.get("table") == "trade" and data.get("action") == "insert"):
        return
    for e in data["data"]:
        e["side"] = e["side"].lower()
        e["created_at"] = now
        print(json.dumps(e))


async def subscribe(ws):
    await ws.send(
        json.dumps(
            {
                "op": "subscribe", "args": "trade:XBTUSD"
            }
        )
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        listen_forever("wss://www.bitmex.com/realtime", subscribe, parse)
    )
    asyncio.get_event_loop().run_forever()
