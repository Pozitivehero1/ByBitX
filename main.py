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

        # проверка старых сделок
        await tracker.run()


        # поиск новых сигналов
        signals = await scanner.run()


        logger.info(
            f"Found signals: {len(signals)}"
        )


        for signal in signals:


            data = await scanner.market.load_symbol(
                signal.symbol
            )


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