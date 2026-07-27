class CandlePatterns:



    @staticmethod
    def analyze(
        df
    ):


        patterns = []



        last = df.iloc[-1]

        prev = df.iloc[-2]



        body = abs(

            last["close"]

            -

            last["open"]

        )



        candle_range = (

            last["high"]

            -

            last["low"]

        )



        if candle_range == 0:

            return patterns



        # Большая зелёная свеча


        if (

            last["close"]

            >

            last["open"]

            and

            body / candle_range > 0.7

        ):


            patterns.append(
                "Strong bullish candle"
            )



        # Большая красная свеча


        if (

            last["close"]

            <

            last["open"]

            and

            body / candle_range > 0.7

        ):


            patterns.append(
                "Strong bearish candle"
            )



        # Поглощение вверх


        if (

            last["close"]

            >

            prev["open"]

            and

            last["open"]

            <

            prev["close"]

        ):


            patterns.append(
                "Bullish engulfing"
            )



        # Поглощение вниз


        if (

            last["close"]

            <

            prev["open"]

            and

            last["open"]

            >

            prev["close"]

        ):


            patterns.append(
                "Bearish engulfing"
            )



        return patterns