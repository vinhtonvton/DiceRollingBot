import discord
import os
import random
import re
import fortune
from dotenv import load_dotenv
import diceCount as dC
import rollDiceTest as rd
from datetime import date
today = date.today()
dateName = "DiceRolled"

load_dotenv()
key = os.getenv("DISCORDKEY")
intents = discord.Intents.default()
intents.message_content= True

no_result_message = 'no mesage lol'

client = discord.Client(intents=intents)
diceCount=dC.RollCounter(dateName)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    diceString = message.content

    userID = message.author.id

    if f'$cleanse' in message.content:
                tempMsg = f"<@{userID}>"
                await message.channel.send(tempMsg +  " Cleansing dice! :salt:\nDice cleansed.")

    if f'$fortune' in message.content:
        random.seed()
        num = random.randint(1, 5)

        tempMsg = fortune.fortune(num, userID)
        await message.channel.send(tempMsg)
    
    #If rolling one die.

    if re.search("\$([0-9]+\+)+", message.content): #Sums stuff up.
        addMsg = message.content.strip("$")
        floatList = addMsg.split("+")
        addFloats = [float(number) for number in floatList]
        await message.channel.send(sum(addFloats))
        

    if f'$D20Stats' in message.content:
        results = diceCount.getD20Count(message.author.id, 20)
        userFormat = f"<@{userID}>\n"
        finalString = userFormat + results
        await message.channel.send(finalString)

    elif f'$D12Stats' in message.content:
        results = diceCount.getD20Count(message.author.id, 12)
        userFormat = f"<@{userID}>\n"
        finalString = userFormat + results
        await message.channel.send(finalString)
        
    elif f'$D10Stats' in message.content:
        results = diceCount.getD20Count(message.author.id, 10)
        userFormat = f"<@{userID}>\n"
        finalString = userFormat + results
        await message.channel.send(finalString)
    elif f'$D8Stats' in message.content:
        results = diceCount.getD20Count(message.author.id, 8)
        userFormat = f"<@{userID}>\n"
        finalString = userFormat + results
        await message.channel.send(finalString)

    elif f'$D6Stats' in message.content:
        results = diceCount.getD20Count(message.author.id, 6)
        userFormat = f"<@{userID}>\n"
        finalString = userFormat + results
        await message.channel.send(finalString)

    elif f'$D4Stats' in message.content:
        results = diceCount.getD20Count(message.author.id, 4)
        userFormat = f"<@{userID}>\n"
        finalString = userFormat + results
        await message.channel.send(finalString)

        
     #Handles rolling dice.
    if '$roll' in message.content:
        diceString = message.content
        diceString = diceString.replace("$roll ", "")
        msgOut = f"<@{userID}>"

        if len(re.findall("d", diceString)) > 1:
            diceArray = diceString.split("+")
            for item in diceArray:
                if "d" in item:
                    msgOut = msgOut + rd.parseDiceString(item, userID)

                else:
                    msgOut = msgOut + "\nModifier: " + item + "\n"

        else:
            msgOut = msgOut + rd.parseDiceString(diceString, userID)

                        
        await message.channel.send(msgOut)

    if '$dc' in message.content:
        await message.channel.send("Disconnecting")
        await client.close()
        exit()



client.run(key)
