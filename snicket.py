import discord
import os
import openai
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
# Access the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API key
openai.api_key = openai_api_key

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$',intents=intents)

@bot.command()
async def hello(ctx):
    await ctx.send('The world is quiet here.')

@bot.command()
async def snicket(ctx):
    await ctx.reply('How do you know who I am?')

@bot.command(pass_context=True)
async def name(ctx):
    username = ctx.message.author.display_name

@bot.event
async def on_message(message):
    #ignore if bot is the author
    if message.author == bot.user:
        return

    # Check if the bot is mentioned in the message
    if bot.user.mentioned_in(message):

        # Process user input and get GPT-3 response
        user_input = message.content
        gpt_response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=user_input,
            max_tokens=150
        )

        # Send GPT-3 response to the same Discord channel
        await message.channel.send(gpt_response.choices[0].text)

bot.run(os.getenv('TOKEN'))