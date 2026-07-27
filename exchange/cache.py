import time



class CandleCache:



    def __init__(
        self,
        ttl=300
    ):

        self.ttl = ttl

        self.data = {}



    def get(
        self,
        key
    ):


        item = self.data.get(
            key
        )


        if not item:

            return None



        if (
            time.time()
            -
            item["time"]
            >
            self.ttl
        ):

            del self.data[key]

            return None



        return item["value"]



    def set(
        self,
        key,
        value
    ):


        self.data[key] = {

            "time":
                time.time(),


            "value":
                value

        }



    def clear(self):

        self.data.clear()
