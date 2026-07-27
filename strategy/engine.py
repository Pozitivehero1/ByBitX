from scanner.ranking import SignalRanking

from strategy.signal import SignalBuilder



class StrategyEngine:



    MIN_SCORE = 85



    @staticmethod
    def analyze(
        symbol,
        data,
        context
    ):


        ranking = (
            SignalRanking
            .calculate(
                data
            )
        )



        if (

            ranking["score"]

            <

            StrategyEngine.MIN_SCORE

        ):

            return None



        signal = (

            SignalBuilder

            .build(

                symbol,

                data["1h"],

                ranking

            )

        )



        if not signal:

            return None



        # фильтр направления рынка


        if (

            signal.direction == "LONG"

            and

            not context.allow_long

        ):


            return None



        if (

            signal.direction == "SHORT"

            and

            not context.allow_short

        ):


            return None



        return signal