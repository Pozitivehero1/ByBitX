from analytics.performance import PerformanceAnalyzer



class AnalyticsReport:



    def __init__(self):

        self.stats = PerformanceAnalyzer()



    def text(self):


        data = self.stats.get_report()



        return f"""

<b>📊 BYBITX BOT REPORT</b>


Всего сигналов:

{data["total"]}


✅ WIN:

{data["wins"]}


❌ LOSS:

{data["losses"]}


⏳ Открыто:

{data["opened"]}


🎯 WinRate:

{data["winrate"]}%


"""