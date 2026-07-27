import json
import os

from config.settings import HISTORY_FILE



class SignalHistory:


    def __init__(self):

        self.file = HISTORY_FILE

        self.create()



    def create(self):

        folder = os.path.dirname(
            self.file
        )


        os.makedirs(
            folder,
            exist_ok=True
        )


        if not os.path.exists(self.file):

            self.save([])



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



    def exists(
        self,
        symbol,
        direction
    ):


        for item in self.load():


            if (

                item.get("symbol") == symbol

                and

                item.get("direction") == direction

            ):

                return True



        return False



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
                    signal.score

            }

        )


        self.save(
            data[-500:]
        )
