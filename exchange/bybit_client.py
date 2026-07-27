import asyncio
import aiohttp

from config.settings import (
    BYBIT_URL,
    CANDLES_LIMIT
)

from utils.logger import logger



class BybitClient:


    def __init__(self):

        self.session = None

        self.semaphore = asyncio.Semaphore(
            10
        )



    async def connect(self):

        timeout = aiohttp.ClientTimeout(
            total=30
        )


        connector = aiohttp.TCPConnector(
            limit=20
        )


        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector
        )



    async def close(self):

        if self.session:

            await self.session.close()



    async def request(
        self,
        endpoint,
        params=None
    ):


        async with self.semaphore:


            url = (
                BYBIT_URL +
                endpoint
            )


            for attempt in range(5):

                try:


                    async with self.session.get(
                        url,
                        params=params
                    ) as response:


                        data = await response.json()



                        if data.get(
                            "retCode"
                        ) != 0:


                            raise Exception(
                                data.get(
                                    "retMsg"
                                )
                            )



                        return data["result"]



                except Exception as e:


                    logger.warning(
                        f"Bybit error {attempt+1}/5: {e}"
                    )


                    await asyncio.sleep(
                        attempt + 1
                    )



            raise Exception(
                "Bybit request failed"
            )



    async def get_symbols(self):


        result = await self.request(

            "/v5/market/instruments-info",

            {

                "category":
                    "linear"

            }

        )


        symbols = []



        for item in result["list"]:


            if item["status"] != "Trading":

                continue


            if item["quoteCoin"] != "USDT":

                continue


            if item["contractType"] != "LinearPerpetual":

                continue



            symbols.append(
                item["symbol"]
            )



        logger.info(
            f"Loaded symbols: {len(symbols)}"
        )


        return symbols



    async def get_klines(
        self,
        symbol,
        interval
    ):


        result = await self.request(

            "/v5/market/kline",

            {

                "category":
                    "linear",


                "symbol":
                    symbol,


                "interval":
                    interval,


                "limit":
                    CANDLES_LIMIT

            }

        )



        candles = []



        for item in reversed(
            result["list"]
        ):


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


        result = await self.request(

            "/v5/market/tickers",

            {

                "category":
                    "linear",


                "symbol":
                    symbol

            }

        )


        return float(
            result["list"][0]["lastPrice"]
        )