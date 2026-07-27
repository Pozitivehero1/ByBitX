# scanner/ranking.py
from scanner.structure import MarketStructure
from scanner.patterns import CandlePatterns

class SignalRanking:
    @staticmethod
    def calculate(data):
        """
        Рассчитывает баллы для LONG и SHORT на основе индикаторов.
        Возвращает направление, общий счёт и список причин.
        """
        df15 = data["15m"]
        df1h = data["1h"]
        df4h = data["4h"]

        last = df1h.iloc[-1]
        last15 = df15.iloc[-1]

        long_score = 0
        short_score = 0
        reasons = []

        # 1. Тренд по 200 EMA (глобальный тренд)
        if last["close"] > last["ema200"]:
            long_score += 20
            reasons.append("Цена выше 200 EMA (бычий тренд)")
        else:
            short_score += 20
            reasons.append("Цена ниже 200 EMA (медвежий тренд)")

        # 2. RSI (перекупленность/перепроданность)
        if last["rsi"] < 30:
            long_score += 20
            reasons.append("RSI перепродан (<30)")
        elif last["rsi"] > 70:
            short_score += 20
            reasons.append("RSI перекуплен (>70)")

        # 3. MACD (гистограмма)
        if last["macd"] > 0:
            long_score += 15
            reasons.append("MACD положительная")
        else:
            short_score += 15
            reasons.append("MACD отрицательная")

        # 4. Мультитаймфреймовое совпадение (1h и 4h)
        trend1h = MarketStructure.detect_trend(df1h)
        trend4h = MarketStructure.detect_trend(df4h)
        if trend1h == "UP" and trend4h == "UP":
            long_score += 20
            reasons.append("Тренд вверх на 1h и 4h")
        elif trend1h == "DOWN" and trend4h == "DOWN":
            short_score += 20
            reasons.append("Тренд вниз на 1h и 4h")

        # 5. Всплеск объёма в направлении движения
        if last["volume_spike"]:
            if last["close"] > last["open"]:  # зелёная свеча
                long_score += 10
                reasons.append("Всплеск объёма на бычьей свече")
            else:
                short_score += 10
                reasons.append("Всплеск объёма на медвежьей свече")

        # 6. Свечные паттерны (только в сторону тренда)
        patterns = CandlePatterns.analyze(df1h)
        for pat in patterns:
            if "bullish" in pat.lower():
                long_score += 5
                reasons.append(pat)
            elif "bearish" in pat.lower():
                short_score += 5
                reasons.append(pat)

        # 7. Подтверждение на 15m (EMA50)
        if last15["close"] > last15["ema50"]:
            long_score += 5
        else:
            short_score += 5

        # Определяем направление
        direction = "LONG" if long_score >= short_score else "SHORT"
        score = max(long_score, short_score)
        score = min(score, 100)  # кап на 100

        return {
            "direction": direction,
            "score": score,
            "reasons": reasons,
            "patterns": patterns
        }
