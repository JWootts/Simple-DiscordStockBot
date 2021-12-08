import os
import finnhub
import discord
import json
from collections import namedtuple
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('API_KEY')
client = discord.Client()
finnhub_client = finnhub.Client(api_key=API_KEY)
NEWLINE = " \n"
STOCKBOT_HELP = " **STOCKBOT HELP**" + NEWLINE + \
                "- !stockbot search [ticker] --> Stock Results" + NEWLINE + \
                "- !stockbot symbol [stockName] --> Search Stock Name Results"


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if str(message.content).__contains__('!stockbot help'):
        await message.channel.send(STOCKBOT_HELP)
        return

    if str(message.content).__contains__('!stockbot search'):
        stockToSearch = str(message.content).replace("!stockbot search", "").strip()
        if stockToSearch != "":
            data = finnhub_client.quote(str(stockToSearch))
            x = json.loads(json.dumps(data), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            await message.channel.send("[**" + stockToSearch + "**] \n" +
                                        "Current Price: $" + str(x.c) + NEWLINE +
                                        "Change: $" + str(x.d) + NEWLINE +
                                        "% Change: " + str(x.dp) + NEWLINE +
                                        "Highest Price of day: $" + str(x.h) + NEWLINE +
                                        "Lowest Price of day $: " + str(x.l) + NEWLINE +
                                        "Open Price: $" + str(x.o) + NEWLINE +
                                        "Previous Close: $" + str(x.pc))
        else:
            await message.channel.send("Invalid stock requested. Please use !stockbot help for more assisatance.")

    elif str(message.content).__contains__('!stockbot symbol'):
        stockToSearch = str(message.content).replace("!stockbot symbol", "").strip()
        returnString = ""
        if stockToSearch != "":
            data = finnhub_client.symbol_lookup(str(stockToSearch))
            x = json.loads(json.dumps(data), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

            for stocks in x.result:
                returnString += "Symbol: " + str(stocks.symbol) + NEWLINE + \
                                "Description: " + str(stocks.description) + NEWLINE + \
                                "Type: " + str(stocks.type) + NEWLINE + NEWLINE

            await message.author.create_dm()
            await message.author.dm_channel.send("Results from search of: '**" + stockToSearch + "**'\n \n" + returnString)
            await message.channel.send("Results have been DM'd to you :)")
        else:
            await message.channel.send("Invalid stock requested. Please use !stockbot help for more assisatance.")

client.run(TOKEN)
