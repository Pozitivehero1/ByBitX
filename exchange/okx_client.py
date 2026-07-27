import aiohttp

from config.settings import CANDLES_LIMIT

from utils.logger import logger



class OKXClient:


    BASE_URL = "https://www.okx.com"



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


        async with self.session.get(

            self.BASE_URL + endpoint,

            params=params

        ) as response:


            data = await response.json()



            if data.get("code") != "0":

                raise Exception(data)



            return data["data"]



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


            if (

                item["settleCcy"]

                ==

                "USDT"

            ):


                symbols.append(

                    item["instId"]

                    .replace("-SWAP","")

                    .replace("-","")

                )



        logger.info(

            f"OKX symbols: {len(symbols)}"

        )



        return symbols



def convert_interval(
    self,
    interval
):


    mapping = {

        "1m": "1m",

        "5m": "5m",

        "15m": "15m",

        "30m": "30m",

        "1h": "1H",

        "4h": "4H",

        "1d": "1D"

    }


    return mapping.get(

        interval,

        "1H"

    )



async def get_klines(
    self,
    symbol,
    interval
):


    okx_symbol = (

        symbol[:-4]

        +

        "-USDT-SWAP"

    )



    bar = self.convert_interval(
        interval
    )



    data = await self.request(

        "/api/v5/market/candles",

        {

            "instId":

                okx_symbol,


            "bar":

                bar,


            "limit":

                str(CANDLES_LIMIT)

        }

    )



    candles = []



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


        okx_symbol = (

            symbol[:-4]

            +

            "-USDT-SWAP"

        )



        data = await self.request(

            "/api/v5/market/candles",

            {

                "instId":

                    okx_symbol,


                "bar":

                    interval,


                "limit":

                    CANDLES_LIMIT

            }

        )



        candles = []



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


        okx_symbol = (

            symbol[:-4]

            +

            "-USDT-SWAP"

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
