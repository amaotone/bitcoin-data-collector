import asyncio
import json

from collector import get_timestamp, parse_bitflyer_timestamp, listen_forever


def parse(data):
    now = get_timestamp()
    for e in data["params"]["message"]:
        e["side"] = e["side"].lower()
        e["amount"] = e["size"]
        e["timestamp"] = parse_bitflyer_timestamp(e["exec_date"])
        del e["exec_date"], e["size"]
        e["created_at"] = now
        print(e)


async def subscribe(ws):
    await ws.send(
        json.dumps(
            {
                "method": "subscribe",
                "params": {"channel": "lightning_executions_FX_BTC_JPY"},
            }
        )
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        listen_forever("wss://ws.lightstream.bitflyer.com/json-rpc", subscribe, parse)
    )
    asyncio.get_event_loop().run_forever()
