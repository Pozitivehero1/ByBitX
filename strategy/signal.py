from strategy.models import Signal

from strategy.risk import RiskManager



class SignalBuilder:



    @staticmethod
    def build(
        symbol,
        df,
        ranking
    ):


        last = df.iloc[-1]



        entry = float(

            last["close"]

        )



        risk = (

            RiskManager

            .calculate(

                entry,

                float(last["atr"]),

                ranking["direction"]

            )

        )



        if risk["risk_reward"] < 2:


            return None



        return Signal(


            symbol=symbol,


            direction=

                ranking["direction"],


            entry=entry,


            stop_loss=

                risk["stop_loss"],


            take_profit_1=

                risk["take_profit_1"],


            take_profit_2=

                risk["take_profit_2"],


            risk_reward=

                risk["risk_reward"],


            score=

                ranking["score"],


            confidence=

                ranking["score"],


            reasons=

                ranking["reasons"],


            pattern=

                ranking["patterns"]

        )