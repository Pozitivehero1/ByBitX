from exchange.bybit_client import BybitClient

from storage.trades import TradeStorage

from utils.logger import logger



class TradeChecker:



    def __init__(self):

        self.client = BybitClient()

        self.storage = TradeStorage()



    async def start(self):

        await self.client.connect()



    async def stop(self):

        await self.client.close()



    async def check(
        self,
        trade
    ):


        price = await self.client.get_price(

            trade["symbol"]

        )



        if trade["direction"] == "LONG":


            if price >= trade["tp"]:

                return "WIN"



            if price <= trade["sl"]:

                return "LOSS"



        if trade["direction"] == "SHORT":


            if price <= trade["tp"]:

                return "WIN"



            if price >= trade["sl"]:

                return "LOSS"



        return "OPEN"



    async def run(self):


        trades = self.storage.load()


        changed = False



        for trade in trades:


            if trade["status"] != "OPEN":

                continue



            try:


                result = await self.check(
                    trade
                )



                if result != "OPEN":


                    trade["status"] = result


                    changed = True



                    logger.info(

                        f"{trade['symbol']} {result}"

                    )



            except Exception as e:


                logger.error(
                    str(e)
                )



        if changed:

            self.storage.save(
                trades
            )