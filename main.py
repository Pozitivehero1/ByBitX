import asyncio

from bot.scanner import MarketScanner
from bot.publisher import Publisher
from tracker.checker import TradeChecker

from utils.logger import logger



async def main():

    scanner = MarketScanner()

    publisher = Publisher()

    tracker = TradeChecker()


    await tracker.start()

    await scanner.start()


    try:


        # проверяем старые сделки

        await tracker.run()



        # ищем новые сигналы

        signals = await scanner.run()



        logger.info(
            f"Found signals: {len(signals)}"
        )



        for signal in signals:


            # ВАЖНО:
            # берём данные уже с индикаторами

            data = await scanner.prepare_data(

                signal.symbol

            )


            if "1h" not in data:

                continue



            await publisher.publish(

                signal,

                data["1h"]

            )



    except Exception as e:


        logger.error(

            f"MAIN ERROR: {e}"

        )



    finally:


        await tracker.stop()

        await scanner.stop()




if __name__ == "__main__":


    asyncio.run(

        main()

    )