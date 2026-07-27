class MarketStructure:



    @staticmethod
    def detect_trend(
        df
    ):


        last = df.iloc[-1]



        previous = df.iloc[-20]



        if (

            last["close"]

            >

            previous["close"]

            and

            last["high"]

            >

            previous["high"]

        ):


            return "UP"



        if (

            last["close"]

            <

            previous["close"]

            and

            last["low"]

            <

            previous["low"]

        ):


            return "DOWN"



        return "SIDE"



    @staticmethod
    def highs_lows(
        df
    ):


        highs = (

            df["high"]

            .rolling(10)

            .max()

        )


        lows = (

            df["low"]

            .rolling(10)

            .min()

        )


        return {


            "high":

                highs.iloc[-1],


            "low":

                lows.iloc[-1]

        }