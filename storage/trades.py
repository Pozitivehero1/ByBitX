import json
import os

from config.settings import STATS_FILE



class TradeStorage:



    def __init__(self):

        self.file = STATS_FILE

        self.create()



    def create(self):


        folder = os.path.dirname(
            self.file
        )


        if folder:

            os.makedirs(
                folder,
                exist_ok=True
            )



        if not os.path.exists(
            self.file
        ):


            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as f:


                json.dump(
                    [],
                    f
                )



    def load(self):

    try:

        with open(
            self.file,
            "r",
            encoding="utf-8"
        ) as f:


            data = json.load(f)


            if isinstance(data, list):

                return data


    except Exception:

        pass



    self.save([])

    return []



    def save(
        self,
        data
    ):


        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False

            )



    def add(
        self,
        signal
    ):


        data = self.load()



        data.append(

            {

                "symbol":

                    signal.symbol,


                "direction":

                    signal.direction,


                "entry":

                    signal.entry,


                "sl":

                    signal.stop_loss,


                "tp":

                    signal.take_profit_2,


                "status":

                    "OPEN"

            }

        )


        self.save(
            data
        )