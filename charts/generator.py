import os

import mplfinance as mpf
import matplotlib.pyplot as plt

from config.settings import CHART_DIR



class ChartGenerator:



    def __init__(self):

        os.makedirs(
            CHART_DIR,
            exist_ok=True
        )



    def create(
        self,
        signal,
        df
    ):


        filename = (

            f"{signal.symbol}_"

            f"{signal.direction}.png"

        )


        path = os.path.join(

            CHART_DIR,

            filename

        )



        data = df.copy()



        data = data.tail(
            120
        )



        data = data.set_index(
            "timestamp"
        )



        entry_line = [

            signal.entry

        ] * len(data)



        sl_line = [

            signal.stop_loss

        ] * len(data)



        tp_line = [

            signal.take_profit_2

        ] * len(data)



        plots = [



            mpf.make_addplot(

                data["ema20"]

            ),



            mpf.make_addplot(

                data["ema50"]

            ),



            mpf.make_addplot(

                data["ema200"]

            ),



            mpf.make_addplot(

                entry_line

            ),



            mpf.make_addplot(

                sl_line

            ),



            mpf.make_addplot(

                tp_line

            )

        ]



        fig, axes = mpf.plot(

            data,

            type="candle",

            volume=True,

            addplot=plots,

            style="yahoo",

            figsize=(10,10),

            title=(

                f"{signal.symbol} "

                f"{signal.direction}"

            ),

            returnfig=True

        )



        fig.savefig(

            path,

            dpi=150,

            bbox_inches="tight"

        )


        plt.close(fig)



        return path