import os

from dotenv import load_dotenv


load_dotenv()



# API

TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN"
)


TELEGRAM_CHANNEL_ID = os.getenv(
    "TELEGRAM_CHANNEL_ID"
)


MISTRAL_API_KEY = os.getenv(
    "MISTRAL_API_KEY"
)



# Bybit

BYBIT_URL = (
    "https://api.bybit.com"
)



CANDLES_LIMIT = 300



TIMEFRAMES = {

    "15m": "15",

    "1h": "60",

    "4h": "240"

}



# Filters


MIN_VOLUME_USDT = 5000000



MAX_SIGNALS_PER_RUN = 3



SIGNAL_COOLDOWN_HOURS = 24



# Storage


HISTORY_FILE = (
    "data/history.json"
)


STATS_FILE = (
    "data/stats.json"
)


CHART_DIR = (
    "data/charts"
)