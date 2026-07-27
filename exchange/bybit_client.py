# exchange/bybit_client.py
import os
import asyncio
import aiohttp
from config.settings import BYBIT_URL, CANDLES_LIMIT
from utils.logger import logger

class BybitClient:
    def __init__(self):
        self.session = None
        self.semaphore = asyncio.Semaphore(10)
        # Читаем прокси из переменной окружения (например, "http://user:pass@host:port")
        self.proxy = os.getenv("BYBIT_PROXY", None)

    async def connect(self):
        timeout = aiohttp.ClientTimeout(total=30)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        # Если указан прокси, передаём его в сессию
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers=headers,
            proxy=self.proxy
        )

    async def close(self):
        if self.session:
            await self.session.close()

    async def request(self, endpoint, params=None):
        async with self.semaphore:
            url = BYBIT_URL + endpoint
            for attempt in range(5):
                try:
                    async with self.session.get(url, params=params) as response:
                        text = await response.text()
                        if response.status != 200:
                            logger.warning(f"Bybit HTTP {response.status}: {text[:200]}")
                            await asyncio.sleep(attempt + 1)
                            continue
                        try:
                            data = await response.json()
                        except Exception:
                            logger.warning(f"Bybit non JSON: {text[:300]}")
                            await asyncio.sleep(attempt + 1)
                            continue
                        if data.get("retCode") != 0:
                            raise Exception(data.get("retMsg"))
                        return data["result"]
                except Exception as e:
                    logger.warning(f"Bybit error {attempt+1}/5: {e}")
                    await asyncio.sleep(attempt + 1)
            raise Exception("Bybit request failed")

    async def get_symbols(self):
        result = await self.request(
            "/v5/market/instruments-info",
            {"category": "linear"}
        )
        symbols = []
        for item in result["list"]:
            if item.get("status") != "Trading":
                continue
            if item.get("quoteCoin") != "USDT":
                continue
            symbols.append(item["symbol"])
        logger.info(f"Loaded symbols: {len(symbols)}")
        return symbols

    async def get_klines(self, symbol, interval):
        result = await self.request(
            "/v5/market/kline",
            {
                "category": "linear",
                "symbol": symbol,
                "interval": interval,
                "limit": CANDLES_LIMIT
            }
        )
        candles = []
        for item in reversed(result["list"]):
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
        result = await self.request(
            "/v5/market/tickers",
            {
                "category": "linear",
                "symbol": symbol
            }
        )
        return float(result["list"][0]["lastPrice"])
