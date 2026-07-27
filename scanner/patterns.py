# scanner/patterns.py
class CandlePatterns:
    @staticmethod
    def analyze(df):
        patterns = []
        last = df.iloc[-1]
        prev = df.iloc[-2]

        body = abs(last["close"] - last["open"])
        candle_range = last["high"] - last["low"]
        if candle_range == 0:
            return patterns

        # Большая свеча (тело > 70% диапазона)
        if body / candle_range > 0.7:
            if last["close"] > last["open"]:
                patterns.append("Strong bullish candle")
            else:
                patterns.append("Strong bearish candle")

        # Бычье поглощение (предыдущая свеча медвежья)
        if (prev["close"] < prev["open"] and
            last["close"] > prev["open"] and
            last["open"] < prev["close"]):
            patterns.append("Bullish engulfing")

        # Медвежье поглощение (предыдущая свеча бычья)
        if (prev["close"] > prev["open"] and
            last["close"] < prev["open"] and
            last["open"] > prev["close"]):
            patterns.append("Bearish engulfing")

        return patterns
