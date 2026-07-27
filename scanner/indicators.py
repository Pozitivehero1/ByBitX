# scanner/indicators.py
import ta

class IndicatorEngine:
    @staticmethod
    def calculate(df):
        data = df.copy()

        # EMA
        data["ema20"] = ta.trend.ema_indicator(data["close"], window=20)
        data["ema50"] = ta.trend.ema_indicator(data["close"], window=50)
        data["ema200"] = ta.trend.ema_indicator(data["close"], window=200)

        # RSI
        data["rsi"] = ta.momentum.rsi(data["close"], window=14)

        # MACD
        macd = ta.trend.MACD(data["close"])
        data["macd"] = macd.macd()
        data["macd_signal"] = macd.macd_signal()

        # ADX
        adx = ta.trend.ADXIndicator(data["high"], data["low"], data["close"])
        data["adx"] = adx.adx()

        # ATR
        atr = ta.volatility.AverageTrueRange(data["high"], data["low"], data["close"])
        data["atr"] = atr.average_true_range()

        # Объём (средний за 20 свечей и всплеск)
        avg_volume = data["volume"].rolling(20).mean()
        data["volume_spike"] = data["volume"] > avg_volume * 1.5

        # Заполняем только пропуски вперёд (не используем bfill, чтобы не искажать последние данные)
        data = data.ffill()
        return data
