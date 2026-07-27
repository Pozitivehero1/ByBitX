import aiohttp

import asyncio


from config.settings import (

    TELEGRAM_TOKEN,

    TELEGRAM_CHANNEL_ID

)



class TelegramClient:



    def __init__(self):

        self.api = (

            f"https://api.telegram.org/bot"

            f"{TELEGRAM_TOKEN}"

        )


        self.channel = TELEGRAM_CHANNEL_ID



    async def send_photo(
        self,
        photo,
        caption
    ):


        url = (

            self.api

            +

            "/sendPhoto"

        )



        for attempt in range(3):


            try:


                form = aiohttp.FormData()



                form.add_field(

                    "chat_id",

                    self.channel

                )


                form.add_field(

                    "caption",

                    caption

                )


                form.add_field(

                    "parse_mode",

                    "HTML"

                )



                with open(

                    photo,

                    "rb"

                ) as file:



                    form.add_field(

                        "photo",

                        file,

                        filename="signal.png",

                        content_type="image/png"

                    )



                    async with aiohttp.ClientSession() as session:


                        async with session.post(

                            url,

                            data=form

                        ) as response:



                            data = await response.json()



                            if data.get("ok"):

                                return True



            except Exception:


                await asyncio.sleep(
                    3
                )



        return False



    async def send_text(
        self,
        text
    ):


        url = (

            self.api

            +

            "/sendMessage"

        )



        payload = {


            "chat_id":

                self.channel,


            "text":

                text,


            "parse_mode":

                "HTML"

        }



        async with aiohttp.ClientSession() as session:


            await session.post(

                url,

                json=payload

            )