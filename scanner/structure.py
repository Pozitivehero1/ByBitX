# scanner/structure.py
class MarketStructure:
    @staticmethod
    def detect_trend(df):
        """
        Определяет тренд на основе цен и скользящих средних.
        Используем EMA50 и EMA20 для большей стабильности.
        """
        last = df.iloc[-1]
        if last["close"] > last["ema50"] and last["ema20"] > last["ema50"]:
            return "UP"
        elif last["close"] < last["ema50"] and last["ema20"] < last["ema50"]:
            return "DOWN"
        return "SIDE"

    @staticmethod
    def highs_lows(df):
        highs = df["high"].rolling(10).max()
        lows = df["low"].rolling(10).min()
        return {"high": highs.iloc[-1], "low": lows.iloc[-1]}
