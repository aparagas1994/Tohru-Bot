from tohru import bot
from random import choice, uniform
from logutils import logger
import datetime
import json
import random
import pickle

IZAFILE = "cache/izamoney.txt"
TAX = 0.05
TIP = 0.15
IZA_USERNAME = "<@191298273779122186>"
IZA_DATE = "8/26/16"

class Data:
    def __init__(self,name,hp):
        self.name = name
        self.hp = hp

@bot.command(name="potato", aliases=["iza","popoto", "lala"], pass_context=True)
async def potato(ctx):
    """Iza (Potato) will take us out to dinner"""


    testObject = Data('Nyx', 45)

    # with open('data_pick2.pkl', 'wb') as pickle_file:
    #     pickle.dump(testObject, pickle_file)


    # with open("data_pick2.pkl", "ab") as pickle_file:
    #     pickle.dump(testObject, pickle_file)

    with open('data_pick2.pkl', 'rb') as pickle_file:
        data = []
        while True:
            try:
                data.append(pickle.load(pickle_file))
            except EOFError:
                break

    # formattingString = "{} has {}HP".format(testObject.name, testObject.hp)
    await ctx.send(data)

    author = ctx.message.author
    now = datetime.datetime.now()
    currenthour = now.hour
    server = ctx.message.server

    moneyFile = IZAFILE
    username = IZA_USERNAME
    date = IZA_DATE


    with open('json/resturant.json') as data_file:
        resturant = json.load(data_file)

    with open(moneyFile,"r") as f:
        totalBefore = float(f.readline())


    online = len([m.status for m in server.members if (str(m.status) == "online" or str(m.status) == "idle") and not m.bot]) - 2 # Don't count Iza or the mentioned
    total = 0.0

    for mealtype, mealinfo in resturant['meals'].items():
        startTime = mealinfo['startTime']
        endTime = mealinfo['endTime']

        if(startTime < endTime and (startTime <= now.hour < endTime)) or \
          (startTime > endTime and (now.hour >= startTime or now.hour < endTime)):
            currentMeal = mealtype
            randResturant = choice(mealinfo['resturants'])
            randResturantName = randResturant['name']
            minprice = randResturant['minPrice']
            maxprice = randResturant['maxPrice']
            break

    logger.debug("Online people: {}".format(online))
    total = sum([uniform(minprice, maxprice) for i in range(online)])
		
    addTaxTotal = total * TAX 
    addTipTotal = total * TIP	

    total = total + addTaxTotal + addTipTotal
    totalSpent = totalBefore + total    

    with open(moneyFile,"w") as f:
        f.write(str(totalSpent) + "\n")    

    response = "{} will buy {} and {} people __***{}***__ at __***{}***__\n".format(username, author.mention, online, currentMeal, randResturantName)
    response += "This Meal: ${:.2f} [Tax: ${:.2f} (5%)   Tip: ${:.2f} (15%)]\n".format(total, addTaxTotal, addTipTotal)
    response += "Min Price: ${:.2f}   Max Price ${:.2f}\n".format(minprice, maxprice)
    response += "Total Spent: **__${:,.2f}__** (Since ".format(totalSpent)
    response += date + ")\n\n"
    response += choice(resturant['responses'])

    # logger.info(response);
    await ctx.send(response)        