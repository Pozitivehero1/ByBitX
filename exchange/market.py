# exchange/market.py
import asyncio
import pandas as pd
from exchange.bybit_client import BybitClient
from exchange.cache import CandleCache
from config.settings import TIMEFRAMES
from utils.logger import logger

class MarketLoader:
    def __init__(self):
        self.client = BybitClient()          # заменили OKXClient на BybitClient
        self.cache = CandleCache()
        self.symbol_limit = asyncio.Semaphore(3)

    async def start(self):
        await self.client.connect()

    async def stop(self):
        await self.client.close()

    async def symbols(self):
        return await self.client.get_symbols()

    async def load_symbol(self, symbol):
        async with self.symbol_limit:
            tasks = []
            for name, interval in TIMEFRAMES.items():
                tasks.append(self.load_timeframe(symbol, name, interval))
            results = await asyncio.gather(*tasks, return_exceptions=True)
            output = {}
            for result in results:
                if isinstance(result, Exception):
                    continue
                name, df = result
                if df is not None:
                    output[name] = df
            return output

    async def load_timeframe(self, symbol, name, interval):
        key = symbol + name
        cached = self.cache.get(key)
        if cached is not None:
            return (name, cached)

        candles = await self.client.get_klines(symbol, interval)

        if not candles:
            return (name, None)

        if len(candles) < 100:
            logger.warning(f"{symbol} {name}: not enough candles")
            return (name, None)

        df = pd.DataFrame(candles)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        self.cache.set(key, df)
        return (name, df)
