# strategy/risk.py
class RiskManager:
    @staticmethod
    def calculate(entry, atr, direction):
        """
        Рассчитывает SL, TP1, TP2 и соотношение риск/прибыль.
        Использует множители ATR с учётом волатильности.
        """
        if atr <= 0:
            return {"risk_reward": 0}

        # Множители можно сделать конфигурируемыми
        sl_mult = 1.5
        tp1_mult = 2.0
        tp2_mult = 4.0

        if direction == "LONG":
            stop_loss = entry - atr * sl_mult
            take_profit_1 = entry + atr * tp1_mult
            take_profit_2 = entry + atr * tp2_mult
        else:  # SHORT
            stop_loss = entry + atr * sl_mult
            take_profit_1 = entry - atr * tp1_mult
            take_profit_2 = entry - atr * tp2_mult

        risk = abs(entry - stop_loss)
        reward = abs(take_profit_2 - entry)
        rr = reward / risk if risk != 0 else 0

        return {
            "stop_loss": round(stop_loss, 8),
            "take_profit_1": round(take_profit_1, 8),
            "take_profit_2": round(take_profit_2, 8),
            "risk_reward": round(rr, 2)
        }
