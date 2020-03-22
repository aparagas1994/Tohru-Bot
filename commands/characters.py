from tohru import bot
from random import choice, uniform
from logutils import logger
from model import CharacterModel
import datetime
import json
import random

@bot.command(name="getCharacter", aliases=["get"], pass_context=True)
async def getcharacters(ctx, *args):
    character = CharacterModel.get(args[0])
    # logger.debug(character)
    # await ctx.send('{}'.format(character.hp))
    response ='{} has been found with {}HP and {}MP'.format(args[0], character.hp, character.mp)
    await ctx.send(response)

@bot.command(name="deleteCharacter", aliases=["delete", "del"], pass_context=True)
async def deleteCharacter(ctx, *args):
    try:
        CharacterModel.get(args[0]).delete()
        await ctx.send("{} has been deleted".format(args[0]))
    except:
        await ctx.send("{} wasn't found".format(args[0]))
    # logger.debug(character)
    # await ctx.send('{}'.format(character.hp))
    # response ='{} has been found with {}HP and {}MP'.format(args[0], character.hp, character.mp)

@bot.command(name="addHP", aliases=["hp"], pass_context=True)
async def addHP(ctx, *args):
    try:
        currentCharacter = CharacterModel.get(args[0])
        currentCharacter.hp = currentCharacter.hp + int(args[1])
        currentCharacter.save()
        await ctx.send("{} now has {}HP".format(args[0],currentCharacter.hp))
    except:
        await ctx.send("{} wasn't found".format(args[0]))
    # logger.debug(character)


@bot.command(name="character", aliases=["add"], pass_context=True)
async def characters(ctx, *args):

    newCharacter = CharacterModel(args[0])
    newCharacter.hp = int(args[1])
    newCharacter.mp = int(args[2])

    newCharacter.save()

    await ctx.send('{} has been saved with {}HP and {}MP'.format(args[0], args[1], args[2]))
    # args = message.content.slice(prefix.length).split(' ');

    """Iza (Potato) will take us out to dinner"""


    # with open('data_pick2.pkl', 'wb') as pickle_file:
    #     pickle.dump(testObject, pickle_file)


    # with open("data_pick2.pkl", "ab") as pickle_file:
    #     pickle.dump(testObject, pickle_file)

    # with open('data_pick2.pkl', 'rb') as pickle_file:
    #     data = []
    #     while True:
    #         try:
    #             data.append(pickle.load(pickle_file))
    #         except EOFError:
    #             break

    # # formattingString = "{} has {}HP".format(testObject.name, testObject.hp)
    # await ctx.send(data)

    # author = ctx.message.author
    # now = datetime.datetime.now()
    # currenthour = now.hour
    # server = ctx.message.server

    # moneyFile = IZAFILE
    # username = IZA_USERNAME
    # date = IZA_DATE

    # online = len([m.status for m in server.members if (str(m.status) == "online" or str(m.status) == "idle") and not m.bot]) - 2 # Don't count Iza or the mentioned
    # total = 0.0

    # for mealtype, mealinfo in resturant['meals'].items():
    #     startTime = mealinfo['startTime']
    #     endTime = mealinfo['endTime']

    #     if(startTime < endTime and (startTime <= now.hour < endTime)) or \
    #       (startTime > endTime and (now.hour >= startTime or now.hour < endTime)):
    #         currentMeal = mealtype
    #         randResturant = choice(mealinfo['resturants'])
    #         randResturantName = randResturant['name']
    #         minprice = randResturant['minPrice']
    #         maxprice = randResturant['maxPrice']
    #         break

    # logger.debug("Online people: {}".format(online))
    # total = sum([uniform(minprice, maxprice) for i in range(online)])
		
    # addTaxTotal = total * TAX 
    # addTipTotal = total * TIP	

    # total = total + addTaxTotal + addTipTotal
    # totalSpent = totalBefore + total    

    # with open(moneyFile,"w") as f:
    #     f.write(str(totalSpent) + "\n")    

    # response = "{} will buy {} and {} people __***{}***__ at __***{}***__\n".format(username, author.mention, online, currentMeal, randResturantName)
    # response += "This Meal: ${:.2f} [Tax: ${:.2f} (5%)   Tip: ${:.2f} (15%)]\n".format(total, addTaxTotal, addTipTotal)
    # response += "Min Price: ${:.2f}   Max Price ${:.2f}\n".format(minprice, maxprice)
    # response += "Total Spent: **__${:,.2f}__** (Since ".format(totalSpent)
    # response += date + ")\n\n"
    # response += choice(resturant['responses'])

    # logger.info(response);
    # await ctx.send('`{}` arguments: `{}`'.format(len(args), ', '.join(args)))
    # await ctx.send('{}'.format(args[0]))