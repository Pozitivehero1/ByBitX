from storage.trades import TradeStorage



class PerformanceAnalyzer:



    def __init__(self):

        self.storage = TradeStorage()



    def get_report(self):


        trades = self.storage.load()



        wins = len(

            [

                x for x in trades

                if x["status"] == "WIN"

            ]

        )



        losses = len(

            [

                x for x in trades

                if x["status"] == "LOSS"

            ]

        )



        opened = len(

            [

                x for x in trades

                if x["status"] == "OPEN"

            ]

        )



        closed = wins + losses



        winrate = 0



        if closed:

            winrate = round(

                wins / closed * 100,

                2

            )



        return {


            "total":

                len(trades),


            "wins":

                wins,


            "losses":

                losses,


            "opened":

                opened,


            "winrate":

                winrate

        }