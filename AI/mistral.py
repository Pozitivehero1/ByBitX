import aiohttp

from config.settings import MISTRAL_API_KEY



class MistralAI:



    def __init__(self):

        self.key = MISTRAL_API_KEY


        self.url = (

            "https://api.mistral.ai/v1/chat/completions"

        )



    async def generate(
        self,
        prompt
    ):


        if not self.key:

            return None



        headers = {


            "Authorization":

                f"Bearer {self.key}",


            "Content-Type":

                "application/json"

        }



        payload = {


            "model":

                "mistral-small-latest",


            "messages":

                [

                    {

                        "role":

                            "user",

                        "content":

                            prompt

                    }

                ],


            "temperature":

                0.4

        }



        async with aiohttp.ClientSession() as session:


            async with session.post(

                self.url,

                headers=headers,

                json=payload

            ) as response:



                data = await response.json()



                try:


                    return (

                        data["choices"][0]

                        ["message"]

                        ["content"]

                    )



                except:


                    return None