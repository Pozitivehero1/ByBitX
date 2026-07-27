import asyncio


from exchange.market import MarketLoader

from scanner.indicators import IndicatorEngine

from scanner.filter import MarketFilter

from strategy.engine import StrategyEngine

from market.context import MarketContextAnalyzer

from storage.history import SignalHistory

from storage.signal_memory import SignalMemory

from utils.logger import logger



class MarketScanner:



    def __init__(self):

        self.market = MarketLoader()

        self.history = SignalHistory()

        self.memory = SignalMemory()



    async def start(self):

        await self.market.start()



    async def stop(self):

        await self.market.stop()



    async def prepare_data(
        self,
        symbol
    ):


        data = await self.market.load_symbol(
            symbol
        )


        for tf in data:


            data[tf] = (

                IndicatorEngine

                .calculate(

                    data[tf]

                )

            )


        return data



    async def get_context(self):


        btc = await self.prepare_data(
            "BTCUSDT"
        )


        eth = await self.prepare_data(
            "ETHUSDT"
        )



        return (

            MarketContextAnalyzer

            .analyze(

                btc["1h"],

                eth["1h"]

            )

        )



    async def scan_symbol(
        self,
        symbol,
        context
    ):


        try:


            data = await self.prepare_data(
                symbol
            )



            if not MarketFilter.validate(
                data["1h"]
            ):

                return None



            signal = (

                StrategyEngine

                .analyze(

                    symbol,

                    data,

                    context

                )

            )



            if not signal:

                return None



            if self.history.exists(

                signal.symbol,

                signal.direction

            ):

                return None



            if not self.memory.can_publish(

                signal.symbol,

                signal.direction

            ):

                return None



            return signal



        except Exception as e:


            logger.error(

                f"{symbol}: {e}"

            )


            return None



    async def run(self):


        context = await self.get_context()



        logger.info(

            f"""

MARKET:
{context.market_direction}

BTC:
{context.btc_trend}

ETH:
{context.eth_trend}

"""

        )



        symbols = await self.market.symbols()



        tasks = []



        for symbol in symbols:


            tasks.append(

                self.scan_symbol(

                    symbol,

                    context

                )

            )



        results = await asyncio.gather(
            *tasks
        )



        signals = [

            x

            for x in results

            if x

        ]



        signals.sort(

            key=lambda x:

            (

                x.score,

                x.risk_reward

            ),

            reverse=True

        )



        return signals[:3]