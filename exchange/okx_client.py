import aiohttp
import asyncio

from config.settings import CANDLES_LIMIT
from utils.logger import logger


class OKXClient:

    BASE_URL = "https://www.okx.com"

    def __init__(self):
        self.session = None
        self.lock = asyncio.Semaphore(5)


    async def connect(self):

        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )


    async def close(self):

        if self.session:
            await self.session.close()


    async def request(
        self,
        endpoint,
        params=None
    ):

        async with self.lock:

            for attempt in range(5):

                async with self.session.get(
                    self.BASE_URL + endpoint,
                    params=params
                ) as response:


                    data = await response.json()


                    if data.get("code") == "0":

                        return data["data"]


                    if data.get("code") in (
                        "50011",
                        "50013"
                    ):

                        logger.warning(
                            "OKX rate limit. Sleep 3s"
                        )

                        await asyncio.sleep(3)

                        continue


                    raise Exception(data)


            raise Exception(
                "OKX request failed after retries"
            )



    async def get_symbols(self):

        data = await self.request(
            "/api/v5/public/instruments",
            {
                "instType": "SWAP"
            }
        )


        symbols = []


        for item in data:

            if (
                item.get("settleCcy") == "USDT"
                and item.get("state") == "live"
            ):

                symbols.append(

                    item["instId"]
                    .replace(
                        "-SWAP",
                        ""
                    )
                    .replace(
                        "-",
                        ""
                    )

                )


        logger.info(
            f"OKX symbols: {len(symbols)}"
        )


        return symbols



    def convert_interval(
        self,
        interval
    ):

        return {

            "1m":"1m",
            "5m":"5m",
            "15m":"15m",
            "30m":"30m",
            "1h":"1H",
            "4h":"4H",
            "1d":"1D"

        }.get(
            interval,
            "1H"
        )



    async def get_klines(
        self,
        symbol,
        interval
    ):


        okx_symbol = (
            symbol.replace(
                "USDT",
                "-USDT-SWAP"
            )
        )


        data = await self.request(

            "/api/v5/market/candles",

            {

                "instId": okx_symbol,

                "bar":
                    self.convert_interval(interval),

                "limit":
                    str(CANDLES_LIMIT)

            }

        )


        candles=[]


        for item in reversed(data):

            candles.append({

                "timestamp":int(item[0]),
                "open":float(item[1]),
                "high":float(item[2]),
                "low":float(item[3]),
                "close":float(item[4]),
                "volume":float(item[5])

            })


        return candles



    async def get_price(
        self,
        symbol
    ):


        okx_symbol = (
            symbol.replace(
                "USDT",
                "-USDT-SWAP"
            )
        )


        data = await self.request(

            "/api/v5/market/ticker",

            {
                "instId":okx_symbol
            }

        )


        return float(
            data[0]["last"]
        )