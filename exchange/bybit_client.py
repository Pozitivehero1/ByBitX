# exchange/bybit_client.py (небольшие улучшения)
import asyncio
import aiohttp
from config.settings import BYBIT_URL, CANDLES_LIMIT
from utils.logger import logger

class BybitClient:
    def __init__(self):
        self.session = None
        self.semaphore = asyncio.Semaphore(10)

    async def connect(self):
        timeout = aiohttp.ClientTimeout(total=30)
        headers = {
            "User-Agent": "Mozilla/5.0 BybitX-Bot",
            "Accept": "application/json"
        }
        self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)

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

    # get_symbols, get_klines, get_price остаются как были
