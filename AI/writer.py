from ai.mistral import MistralAI



class SignalWriter:



    def __init__(self):

        self.ai = MistralAI()



    async def create_text(
        self,
        signal
    ):


        prompt = f"""

Ты криптовалютный аналитик.


Создай короткий комментарий для Telegram.


Монета:

{signal.symbol}


Направление:

{signal.direction}


Score:

{signal.score}/100


Причины:

{", ".join(signal.reasons)}



Правила:

- максимум 3 предложения;
- без обещаний прибыли;
- без слова гарантия;
- профессиональный стиль.


"""



        result = await self.ai.generate(
            prompt
        )



        if result:

            return result



        return (

            "Сигнал сформирован "

            "на основе технического анализа, "

            "объёма и структуры рынка."

        )