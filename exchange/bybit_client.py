# exchange/bybit_client.py
import os
import asyncio
from pybit.unified_trading import HTTP
from config.settings import CANDLES_LIMIT
from utils.logger import logger

class BybitClient:
    def __init__(self):
        self.session = None
        self.proxy = os.getenv("BYBIT_PROXY", None)

    async def connect(self):
        """Создаёт синхронное подключение (HTTP)."""
        self.session = HTTP(
            testnet=False,
            proxy=self.proxy,
        )

    async def close(self):
        """Закрывать нечего, но оставляем для совместимости."""
        self.session = None

    async def _run_sync(self, method, *args, **kwargs):
        """Выполняет синхронный метод в отдельном потоке."""
        return await asyncio.to_thread(method, *args, **kwargs)

    async def get_symbols(self):
        result = await self._run_sync(
            self.session.get_instruments_info,
            category="linear"
        )
        symbols = []
        for item in result["result"]["list"]:
            if item["status"] == "Trading" and item["quoteCoin"] == "USDT":
                symbols.append(item["symbol"])
        logger.info(f"Loaded symbols: {len(symbols)}")
        return symbols

    async def get_klines(self, symbol, interval):
        result = await self._run_sync(
            self.session.get_kline,
            category="linear",
            symbol=symbol,
            interval=interval,
            limit=CANDLES_LIMIT
        )
        candles = []
        for item in reversed(result["result"]["list"]):
            candles.append({
                "timestamp": int(item[0]),
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5])
            })
        return candles

    async def get_price(self, symbol):
        result = await self._run_sync(
            self.session.get_tickers,
            category="linear",
            symbol=symbol
        )
        return float(result["result"]["list"][0]["lastPrice"])
