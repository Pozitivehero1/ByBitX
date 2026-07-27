import json
import os
import time

from config.settings import SIGNAL_COOLDOWN_HOURS



class SignalMemory:



    def __init__(self):

        self.file = (
            "data/signal_memory.json"
        )

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

        with open(
            self.file,
            "r",
            encoding="utf-8"
        ) as f:


            return json.load(
                f
            )



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



    def can_publish(
        self,
        symbol,
        direction
    ):


        now = time.time()


        data = self.load()



        for item in data:


            if (

                item["symbol"] == symbol

                and

                item["direction"] == direction

            ):


                hours = (

                    now - item["time"]

                ) / 3600



                if hours < SIGNAL_COOLDOWN_HOURS:

                    return False



        return True



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


                "score":

                    signal.score,


                "time":

                    time.time()

            }

        )



        self.save(

            data[-1000:]

        )