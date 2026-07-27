import aiohttp
import asyncio
import time

from config.settings import CANDLES_LIMIT
from utils.logger import logger


class OKXClient:

    BASE_URL = "https://www.okx.com"


    def __init__(self):

        self.session = None

        self.request_lock = asyncio.Lock()

        self.last_request_time = 0

        # около 8 запросов в секунду
        self.delay = 0.13



    async def connect(self):

        self.session = aiohttp.ClientSession(

            headers={
                "User-Agent": "Mozilla/5.0"
            }

        )



    async def close(self):

        if self.session:

            await self.session.close()



    async def _wait_rate_limit(self):

        async with self.request_lock:

            now = time.time()

            diff = now - self.last_request_time


            if diff < self.delay:

                await asyncio.sleep(
                    self.delay - diff
                )


            self.last_request_time = time.time()



    async def request(
        self,
        endpoint,
        params=None
    ):


        for attempt in range(6):


            await self._wait_rate_limit()


            async with self.session.get(

                self.BASE_URL + endpoint,

                params=params

            ) as response:


                data = await response.json()



                if data.get("code") == "0":

                    return data["data"]



                code = data.get("code")



                if code in (
                    "50011",
                    "50013"
                ):


                    sleep_time = (
                        2 + attempt * 2
                    )


                    logger.warning(

                        f"OKX rate limit. Sleep {sleep_time}s"

                    )


                    await asyncio.sleep(
                        sleep_time
                    )


                    continue



                raise Exception(data)



        raise Exception(
            "OKX request failed"
        )



    async def get_symbols(self):


        data = await self.request(

            "/api/v5/public/instruments",

            {
                "instType":"SWAP"
            }

        )


        symbols=[]


        for item in data:


            if (

                item.get("settleCcy") == "USDT"

                and

                item.get("state") == "live"

            ):


                symbol = (

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


                symbols.append(symbol)



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


        okx_symbol = symbol.replace(

            "USDT",

            "-USDT-SWAP"

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

                "timestamp":
                    int(item[0]),

                "open":
                    float(item[1]),

                "high":
                    float(item[2]),

                "low":
                    float(item[3]),

                "close":
                    float(item[4]),

                "volume":
                    float(item[5])

            })



        return candles



    async def get_price(
        self,
        symbol
    ):


        okx_symbol=symbol.replace(

            "USDT",

            "-USDT-SWAP"

        )



        data = await self.request(

            "/api/v5/market/ticker",

            {

                "instId": okx_symbol

            }

        )


        return float(

            data[0]["last"]

        )