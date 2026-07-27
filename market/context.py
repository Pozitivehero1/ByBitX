from dataclasses import dataclass



@dataclass
class MarketContext:


    btc_trend: str

    eth_trend: str

    market_direction: str

    allow_long: bool

    allow_short: bool

    reasons: list




class MarketContextAnalyzer:



    @staticmethod
    def detect(
        df
    ):


        last = df.iloc[-1]



        if (

            last["close"]

            >

            last["ema200"]

            and

            last["ema20"]

            >

            last["ema50"]

        ):


            return "UP"



        if (

            last["close"]

            <

            last["ema200"]

            and

            last["ema20"]

            <

            last["ema50"]

        ):


            return "DOWN"



        return "SIDE"



    @classmethod
    def analyze(
        cls,
        btc,
        eth
    ):


        btc_trend = cls.detect(
            btc
        )


        eth_trend = cls.detect(
            eth
        )



        reasons = []



        allow_long = True

        allow_short = True



        if btc_trend == "DOWN":


            allow_long = False


            reasons.append(
                "BTC downtrend"
            )



        if btc_trend == "UP":


            allow_short = False


            reasons.append(
                "BTC uptrend"
            )



        if (

            btc_trend == "UP"

            and

            eth_trend == "UP"

        ):


            market = "BULL"



        elif (

            btc_trend == "DOWN"

            and

            eth_trend == "DOWN"

        ):


            market = "BEAR"



        else:


            market = "SIDE"



        return MarketContext(


            btc_trend=btc_trend,


            eth_trend=eth_trend,


            market_direction=market,


            allow_long=allow_long,


            allow_short=allow_short,


            reasons=reasons

        )