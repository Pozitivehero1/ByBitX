import aiohttp
import asyncio

from config.settings import CANDLES_LIMIT

from utils.logger import logger



class BinanceClient:


    BASE_URL = (
        "https://fapi.binance.com"
    )


    def __init__(self):

        self.session = None



    async def connect(self):

        self.session = aiohttp.ClientSession(

            headers={

                "User-Agent":
                    "Mozilla/5.0"

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


        url = (

            self.BASE_URL

            +

            endpoint

        )


        async with self.session.get(

            url,

            params=params

        ) as response:


            data = await response.json()


            if response.status != 200:

                raise Exception(data)



            return data



    async def get_symbols(self):


        data = await self.request(

            "/fapi/v1/exchangeInfo"

        )


        symbols = []



        for item in data["symbols"]:


            if (

                item["quoteAsset"]

                ==

                "USDT"

                and

                item["status"]

                ==

                "TRADING"

            ):


                symbols.append(

                    item["symbol"]

                )



        logger.info(

            f"Binance symbols: {len(symbols)}"

        )


        return symbols



    async def get_klines(
        self,
        symbol,
        interval
    ):


        data = await self.request(

            "/fapi/v1/klines",

            {

                "symbol":

                    symbol,


                "interval":

                    interval,


                "limit":

                    CANDLES_LIMIT

            }

        )



        candles = []



        for item in data:


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


        data = await self.request(

            "/fapi/v1/ticker/price",

            {

                "symbol":

                    symbol

            }

        )


        return float(

            data["price"]

        )