# exchange/bybit_client.py
import os
from pybit.unified_trading import AsyncHTTP
from config.settings import CANDLES_LIMIT
from utils.logger import logger

class BybitClient:
    def __init__(self):
        self.session = None
        # Читаем прокси из переменной окружения (если есть)
        self.proxy = os.getenv("BYBIT_PROXY", None)

    async def connect(self):
        """Создаёт асинхронное подключение к Bybit."""
        self.session = AsyncHTTP(
            testnet=False,          # False = основная торговая сеть
            proxy=self.proxy,       # Если прокси не задан, будет None (без прокси)
        )

    async def close(self):
        """Закрывает сессию."""
        if self.session:
            await self.session.close()

    async def get_symbols(self):
        """Возвращает список всех торговых пар USDT."""
        result = await self.session.get_instruments_info(category="linear")
        symbols = []
        for item in result["result"]["list"]:
            if item["status"] == "Trading" and item["quoteCoin"] == "USDT":
                symbols.append(item["symbol"])
        logger.info(f"Loaded symbols: {len(symbols)}")
        return symbols

    async def get_klines(self, symbol, interval):
        """Возвращает свечи для символа и интервала."""
        result = await self.session.get_kline(
            category="linear",
            symbol=symbol,
            interval=interval,
            limit=CANDLES_LIMIT
        )
        candles = []
        # Bybit возвращает свечи в порядке от новых к старым, разворачиваем
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
        """Возвращает текущую цену символа."""
        result = await self.session.get_tickers(category="linear", symbol=symbol)
        return float(result["result"]["list"][0]["lastPrice"])
