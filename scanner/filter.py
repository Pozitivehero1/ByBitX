from config.settings import MIN_VOLUME_USDT



class MarketFilter:


    @staticmethod
    def validate(df):


        if len(df) < 50:

            return False



        last = df.iloc[-1]


        if last["volume"] < MIN_VOLUME_USDT:

            return False



        volatility = (

            df["close"]

            .pct_change()

            .tail(20)

            .abs()

            .mean()

        )


        if volatility < 0.0005:

            return False



        return True