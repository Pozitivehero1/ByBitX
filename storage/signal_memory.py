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

            self.save([])



    def load(self):

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:


                data = json.load(f)



                if isinstance(
                    data,
                    list
                ):

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



    def can_publish(
        self,
        symbol,
        direction
    ):


        now = time.time()



        signals = self.load()



        for item in signals:


            if (

                item.get("symbol")

                ==

                symbol

                and

                item.get("direction")

                ==

                direction

            ):


                hours = (

                    now

                    -

                    item.get(
                        "time",
                        0
                    )

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