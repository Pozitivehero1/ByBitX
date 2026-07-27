# scanner/filter.py
from config.settings import MIN_VOLUME_USDT

class MarketFilter:
    @staticmethod
    def validate(df):
        """
        Проверяет, подходит ли монета для анализа:
        - достаточно свечей
        - объём в USDT выше порога
        - минимальная волатильность
        """
        if len(df) < 50:
            return False

        last = df.iloc[-1]
        # Объём в USDT = объём контрактов * цена закрытия (для OKX)
        volume_usdt = last["volume"] * last["close"]
        if volume_usdt < MIN_VOLUME_USDT:
            return False

        volatility = df["close"].pct_change().tail(20).abs().mean()
        if volatility < 0.0005:
            return False

        return True
