from analytics.report import AnalyticsReport

from telegram.client import TelegramClient



class ReportJob:



    def __init__(self):

        self.report = AnalyticsReport()

        self.telegram = TelegramClient()



    async def run(self):


        text = (

            self.report

            .text()

        )


        await self.telegram.send_text(

            text

        )