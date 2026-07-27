from AI.writer import SignalWriter

from charts.generator import ChartGenerator

from charts.template import ChartTemplate

from telegram.client import TelegramClient

from storage.history import SignalHistory

from storage.signal_memory import SignalMemory

from storage.trades import TradeStorage



class Publisher:



    def __init__(self):

        self.writer = SignalWriter()

        self.chart = ChartGenerator()

        self.telegram = TelegramClient()

        self.history = SignalHistory()

        self.memory = SignalMemory()

        self.trades = TradeStorage()



    async def publish(
        self,
        signal,
        df
    ):


        text = await self.writer.create_text(
            signal
        )


        image = self.chart.create(

            signal,

            df

        )


        image = ChartTemplate.add_header(

            image,

            signal

        )



        caption = f"""

<b>🚨 BYBITX SIGNAL</b>


<b>#{signal.symbol}</b>


📌 <b>{signal.direction}</b>


💰 Entry:

<code>{signal.entry}</code>


🎯 TP1:

<code>{signal.take_profit_1}</code>


🎯 TP2:

<code>{signal.take_profit_2}</code>


🛑 SL:

<code>{signal.stop_loss}</code>


⚖️ RR:

<b>{signal.risk_reward}</b>


🔥 Score:

<b>{signal.score}/100</b>


🤖 AI:

{text}



⚠️ Не является финансовой рекомендацией

"""



        await self.telegram.send_photo(

            image,

            caption

        )



        self.history.add(
            signal
        )


        self.memory.add(
            signal
        )


        self.trades.add(
            signal
        )
