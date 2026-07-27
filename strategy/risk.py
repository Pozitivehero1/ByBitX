class RiskManager:



    @staticmethod
    def calculate(
        entry,
        atr,
        direction
    ):


        if atr <= 0:


            return {


                "risk_reward":0

            }



        sl_distance = atr * 1.8

        tp1_distance = atr * 2

        tp2_distance = atr * 4



        if direction == "LONG":


            stop_loss = (

                entry

                -

                sl_distance

            )


            take_profit_1 = (

                entry

                +

                tp1_distance

            )


            take_profit_2 = (

                entry

                +

                tp2_distance

            )



        else:


            stop_loss = (

                entry

                +

                sl_distance

            )


            take_profit_1 = (

                entry

                -

                tp1_distance

            )


            take_profit_2 = (

                entry

                -

                tp2_distance

            )



        risk = abs(

            entry

            -

            stop_loss

        )


        reward = abs(

            take_profit_2

            -

            entry

        )


        rr = reward / risk



        return {


            "stop_loss":

                round(stop_loss,8),


            "take_profit_1":

                round(take_profit_1,8),


            "take_profit_2":

                round(take_profit_2,8),


            "risk_reward":

                round(rr,2)

        }