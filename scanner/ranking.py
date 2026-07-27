from scanner.structure import MarketStructure
from scanner.patterns import CandlePatterns



class SignalRanking:



    @staticmethod
    def calculate(
        data
    ):


        long_score = 0

        short_score = 0

        reasons = []



        df15 = data["15m"]

        df1h = data["1h"]

        df4h = data["4h"]



        last = df1h.iloc[-1]



        # EMA TREND

        if (

            last["ema20"]

            >

            last["ema50"]

            >

            last["ema200"]

        ):


            long_score += 20

            reasons.append(
                "EMA bullish trend"
            )



        elif (

            last["ema20"]

            <

            last["ema50"]

            <

            last["ema200"]

        ):


            short_score += 20

            reasons.append(
                "EMA bearish trend"
            )



        # RSI


        if 45 <= last["rsi"] <= 65:


            long_score += 10

            reasons.append(
                "RSI LONG zone"
            )



        elif 35 <= last["rsi"] <= 55:


            short_score += 10

            reasons.append(
                "RSI SHORT zone"
            )



        # MACD


        if (

            last["macd"]

            >

            last["macd_signal"]

        ):


            long_score += 15

            reasons.append(
                "MACD bullish"
            )


        else:


            short_score += 15

            reasons.append(
                "MACD bearish"
            )



        # ADX


        if last["adx"] > 25:


            long_score += 10

            short_score += 10


            reasons.append(
                "Strong trend"
            )



        # Volume


        if last["volume_spike"]:


            long_score += 10

            short_score += 10


            reasons.append(
                "Volume spike"
            )



        # Structure


        trend1h = (
            MarketStructure
            .detect_trend(
                df1h
            )
        )


        trend4h = (
            MarketStructure
            .detect_trend(
                df4h
            )
        )



        if (

            trend1h == "UP"

            and

            trend4h == "UP"

        ):


            long_score += 20

            reasons.append(
                "Multi timeframe bullish"
            )



        elif (

            trend1h == "DOWN"

            and

            trend4h == "DOWN"

        ):


            short_score += 20

            reasons.append(
                "Multi timeframe bearish"
            )



        # Candles


        patterns = (
            CandlePatterns
            .analyze(
                df1h
            )
        )



        if patterns:


            long_score += 5

            short_score += 5


            reasons.extend(
                patterns
            )



        # 15m confirmation


        last15 = df15.iloc[-1]


        if (

            last15["close"]

            >

            last15["ema50"]

        ):


            long_score += 10



        else:


            short_score += 10



        if long_score > short_score:


            direction = "LONG"

            score = long_score



        else:


            direction = "SHORT"

            score = short_score



        return {


            "direction":

                direction,


            "score":

                min(score,100),


            "reasons":

                reasons,


            "patterns":

                patterns

        }