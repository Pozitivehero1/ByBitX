import aiohttp
import asyncio
import random

from config.settings import CANDLES_LIMIT
from utils.logger import logger


class OKXClient:

    BASE_URL = "https://www.okx.com"


    def __init__(self):

        self.session = None

        self.rate_limit = asyncio.Semaphore(2)



    async def connect(self):

        self.session = aiohttp.ClientSession(

            headers={
                "User-Agent":
                    "Mozilla/5.0"
            },

            timeout=aiohttp.ClientTimeout(
                total=15
            )

        )



    async def close(self):

        if self.session:

            await self.session.close()



    def format_symbol(self, symbol):

        if "-SWAP" in symbol:

            return symbol

        if "-" in symbol:

            return symbol + "-SWAP"

        return symbol.replace(
            "USDT",
            "-USDT-SWAP"
        )



    async def request(
        self,
        endpoint,
        params=None
    ):


        async with self.rate_limit:


            for attempt in range(5):

                try:

                    async with self.session.get(

                        self.BASE_URL + endpoint,

                        params=params

                    ) as response:


                        data = await response.json()



                        if data.get("code") == "0":

                            return data["data"]



                        if data.get("code") == "50011":

                            wait = (
                                3 + attempt * 3
                            )

                            logger.warning(

                                f"OKX rate limit. Sleep {wait}s"

                            )

                            await asyncio.sleep(wait)

                            continue



                        raise Exception(data)



                except Exception as e:


                    if attempt == 4:

                        raise e


                    await asyncio.sleep(

                        random.uniform(
                            1,
                            3
                        )

                    )



    async def get_symbols(self):


        data = await self.request(

            "/api/v5/public/instruments",

            {
                "instType":
                    "SWAP"
            }

        )


        symbols = []



        for item in data:


            if item.get("settleCcy") == "USDT":


                symbols.append(

                    item["instId"]
                    .replace("-","")
                    .replace("SWAP","")

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


        okx_symbol = self.format_symbol(
            symbol
        )


        data = await self.request(

            "/api/v5/market/candles",

            {

                "instId":
                    okx_symbol,

                "bar":
                    self.convert_interval(interval),

                "limit":
                    str(CANDLES_LIMIT)

            }

        )


        candles=[]


        for item in reversed(data):


            candles.append(

                {

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

                }

            )


        return candles



    async def get_price(
        self,
        symbol
    ):


        okx_symbol = self.format_symbol(
            symbol
        )


        data = await self.request(

            "/api/v5/market/ticker",

            {

                "instId":
                    okx_symbol

            }

        )


        return float(

            data[0]["last"]

        )