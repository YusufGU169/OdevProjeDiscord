import discord
from discord.ext import commands
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from random import *
from modelim import *
from banaait import *
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')
@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)
@bot.command()
async def elhareketleri(ctx):
    if ctx.message.attachments:
        for elhareketresim in ctx.message.attachments:
            eh_ismi = elhareketresim.filename
            eh_url = elhareketresim.url
            await elhareketresim.save(f"./{elhareketresim.filename}")
            # Disable scientific notation for clarity
            np.set_printoptions(suppress=True)
            # Load the model
            model = load_model("keras_model2.h5", compile=False)
            # Load the labels
            class_names = open("labels2.txt", "r").readlines()
            # Create the array of the right shape to feed into the keras model
            # The 'length' or number of images you can put into the array is
            # determined by the first position in the shape tuple, in this case 1
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            # Replace this with the path to your image
            image = Image.open(eh_ismi).convert("RGB")
            # resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            # turnthe image into a numpy array
            image_array = np.asarray(image)
            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            # Load the image into the array
            data[0] = normalized_image_array
            # Predicts the model
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]
            secilen_sinif = class_name[2:]
            if secilen_sinif == "OK\n":
                cwrite = ("OK")
            elif secilen_sinif == "iyi\n":
                cwrite = ("iyi")
            elif secilen_sinif == "Kotu\n":
                cwrite = ("Kotu")
            elif secilen_sinif == "1\n":
                cwrite = ("1")
            elif secilen_sinif == "Rock\n":
                cwrite = ("Rock")
            elif secilen_sinif == "5 / El\n":
                cwrite = ("5 / El")
        await ctx.send(cwrite)
bot.run(jetonum)