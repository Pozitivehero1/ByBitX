from config.settings import MIN_VOLUME_USDT



class MarketFilter:



    @staticmethod
    def validate(
        df
    ):


        if len(df) < 200:

            return False



        last = df.iloc[-1]



        # слишком маленький объём


        if last["volume"] < MIN_VOLUME_USDT:

            return False



        # нет движения


        volatility = (

            abs(

                df["close"]

                .pct_change()

                .tail(20)

            )

            .mean()

        )



        if volatility < 0.001:

            return False



        return True