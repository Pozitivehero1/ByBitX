from dataclasses import dataclass



@dataclass
class Signal:


    symbol: str

    direction: str

    entry: float

    stop_loss: float

    take_profit_1: float

    take_profit_2: float

    risk_reward: float

    score: int

    confidence: int

    reasons: list

    pattern: list