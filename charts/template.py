from PIL import Image, ImageDraw, ImageFont



class ChartTemplate:



    @staticmethod
    def add_header(
        image_path,
        signal
    ):


        image = Image.open(
            image_path
        )


        draw = ImageDraw.Draw(
            image
        )


        try:


            font_big = ImageFont.truetype(

                "arial.ttf",

                50

            )


            font = ImageFont.truetype(

                "arial.ttf",

                30

            )


        except:


            font_big = None

            font = None



        header = (

            "BYBITX SIGNAL"

        )



        draw.text(

            (40,30),

            header,

            font=font_big,

            fill="white"

        )



        info = f"""

#{signal.symbol}


{signal.direction}


ENTRY:

{signal.entry}


TP:

{signal.take_profit_2}


SL:

{signal.stop_loss}


RR:

{signal.risk_reward}


SCORE:

{signal.score}/100

"""



        draw.text(

            (50,100),

            info,

            font=font,

            fill="white"

        )



        image.save(

            image_path

        )


        return image_path