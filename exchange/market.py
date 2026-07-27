import asyncio

import pandas as pd

from exchange.okx_client import OKXClient

from exchange.cache import CandleCache

from config.settings import TIMEFRAMES



class MarketLoader:



    def __init__(self):

        self.client = OKXClient()

        self.cache = CandleCache()



    async def start(self):

        await self.client.connect()



    async def stop(self):

        await self.client.close()



    async def symbols(self):

        return await self.client.get_symbols()



    async def load_symbol(
        self,
        symbol
    ):


        tasks = []


        for name, interval in TIMEFRAMES.items():


            tasks.append(

                self.load_timeframe(

                    symbol,

                    name,

                    interval

                )

            )



        results = await asyncio.gather(
            *tasks
        )



        output = {}



        for name, df in results:

            output[name] = df



        return output



    async def load_timeframe(
        self,
        symbol,
        name,
        interval
    ):


        key = (
            symbol +
            name
        )



        cached = self.cache.get(
            key
        )



        if cached is not None:

            return (
                name,
                cached
            )



        candles = await self.client.get_klines(

            symbol,

            interval

        )



        df = pd.DataFrame(
            candles
        )



        df["timestamp"] = pd.to_datetime(

            df["timestamp"],

            unit="ms"

        )



        self.cache.set(
            key,
            df
        )



        return (
            name,
            df
        )
