from scanner.ranking import SignalRanking
from strategy.signal import SignalBuilder



class StrategyEngine:


    MIN_SCORE = 60



    @staticmethod
    def analyze(
        symbol,
        data,
        context
    ):


        ranking = SignalRanking.calculate(

            data

        )


        score = ranking.get(

            "score",

            0

        )



        if score < StrategyEngine.MIN_SCORE:

            return None



        signal = SignalBuilder.build(

            symbol,

            data["1h"],

            ranking

        )


        if not signal:

            return None



        if signal.direction == "LONG":

            if not context.allow_long:

                return None



        if signal.direction == "SHORT":

            if not context.allow_short:

                return None



        return signal