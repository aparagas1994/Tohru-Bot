from collections import defaultdict
from tohru import bot
from random import choice, uniform, randint, shuffle
from logutils import logger
from sigterm_handler import register_sigterm_handler
import json
import discord

jsonFile = 'json/astro.json'
with open(jsonFile) as data_file:
    astro = json.load(data_file)

balance_dict = defaultdict(int)
BALANCE_COUNT = "cache/balancecounter.json"

naotaID = "157309494181756928"
tohruID = "288042810140262403"
tokiID = "158381388255461376"
akizukiID = "291687380858044420"

try:
    with open(BALANCE_COUNT) as balance_data:
        balance_json = json.load(balance_data)
        for id, count in balance_json.items():
            balance_dict[id] = count
        logger.debug(balance_dict)
except Exception:
    logger.debug("File not found, creating a new file")

@register_sigterm_handler()
def dump_balance_dict():
    with open(BALANCE_COUNT, "w") as balance_data:
        json.dump(dict(balance_dict), balance_data)

def randomcards(selectedID):
    randTimeStatusName = "."
    randTimeEmoji = ""
    selectedSpreadList = ""
    balance_found = False
    expanded_found = False

    # Get random card here
    cardStatus = astro['astrocards']
    randCard = choice(cardStatus['cards'])
    randCardName = randCard['name']
    randCardEmoji = randCard['emoji']
    randEffect = choice(cardStatus['effects'])
    randEffectName = randEffect['saying']
    randEffectEmoji = randEffect['emoji']
    randTimeStatus = choice(cardStatus['timeExtend'])

    if selectedID == naotaID:
        for x in range(5):
            if randCardName == "Balance":
                randCardName, randCardEmoji = reroll()
            else:
                break

    if selectedID == tohruID or selectedID == tokiID:
    #    if selectedID == tohruID:
    #        formattedName = "me"
        for x in range(6):
            if randCardName != "Balance":
                randCardName, randCardEmoji = reroll()
            else:
                break

    if randCardName == "Balance":
        balance_dict[selectedID] += 1
        balance_found = True

    if randEffectName == "an expanded":
        expanded_found = True

    if(randint(0,100) >= 70): # 30% chance for a special time boosting effect ability
        randTimeStatusName = randTimeStatus['name']
        randTimeEmoji = randTimeStatus['emoji']

    response = "{} **{}**{}  {}{}{}".format(randEffectName.title(), 
        randCardName, randTimeStatusName, randCardEmoji, randEffectEmoji, randTimeEmoji) 
    return response, balance_found, expanded_found

def reroll():
    cardStatus = astro['astrocards']
    randCard = choice(cardStatus['cards'])
    randCardName = randCard['name']
    randCardEmoji = randCard['emoji']

    return randCardName, randCardEmoji
  

#Start
@bot.command(name="balance", aliases=["astro", "ast", "Ast"], pass_context=True)
async def balance(ctx, user : discord.Member=None, astLoop : int=None):
    author = ctx.message.author
    server = ctx.message.server
    tohruBalance = False
    tokiBalance = False
    anybodyBalance = False
    balance_found = False
    astLoopCount = 0
    cardList = []

    if astLoop == None or int(astLoop) <= 0:
        astLoopCount = 1
    else:
        astLoopCount = int(astLoop)
        if(astLoopCount > 5):
            await bot.say("I can only do a max of 5 cards ^w^'")
            astLoopCount = 5

    grabMembers = [member for member in bot.get_all_members() if (str(member.status) == "online" or str(member.status) == "idle") and member.server is server]
    minMembers = min(2, len(grabMembers))
    maxMembers = min(5, len(grabMembers))
    balance_found = False
    expand_found = False
    
    for currentLoop in range(0, astLoopCount):

        if user == None:
            selectedPerson = choice(grabMembers)
            selectedName = selectedPerson.name
            selectedID = selectedPerson.id
        else:
            selectedName = user.name
            selectedID = user.id

        cards, balance_trigger, expanded_trigger = randomcards(selectedID)
        cardList.append(cards)
        balance_found = balance_found or balance_trigger
        expand_found = expand_found or expanded_trigger

    #Outside For Loop
    formattedName = selectedName
    if(author.name == selectedName):
        formattedName = "themself"

    response = "{} gives {} ".format(author.name, formattedName)
    if(len(cardList) > 1): #Koryuu gives me an expanded Balance with Time Dilation & Celestial Opposition!
        response += "the following:\n".format(author.name, formattedName)
    response += '\n'.join(cardList)
    response += "\n\n{}'s Total Balances: {}".format(selectedName, balance_dict[selectedID])

    if expand_found:
        # selectedName = Naota
        # grabMembers = [Koryuu, Kyonko, Naota, Iza, Vale, Yin, Tohru, Kupo]
        shuffle(grabMembers) # [Naota, Kyonko, Koryuu, Kupo, Iza, Tohru, Vale]
        # grabMembers = filter(lambda member: member.id is not selectedID, grabMembers) 
        grabMembers = [member for member in grabMembers if member.id not in [selectedID, naotaID]] # [Kyonko, Koryuu, Kupo, Iza, Tohru, Vale], # [Kyonko, Koryuu, Kupo, Iza, Tohru, Vale], filter(lambda member: member.id is not selectedID, grabMembers)
        selectedSpreadList = []
        selectedIndex = 0
        for x in range(randint(minMembers, maxMembers)): # Assuming range(3)
            selectedSpreadList.append(grabMembers[selectedIndex])
            if balance_found == "Balance":
                balance_dict[grabMembers[selectedIndex].id] += 1
            selectedIndex += 1 # [Kyonko, Koryuu, Kupo]
        selectedSpreadString = ", ".join([member.name for member in selectedSpreadList]) # Kyonko, Koryuu, Kupo                        
        response += "\n\nShared with: {}\n".format(selectedSpreadString)

    await bot.say(response)

    if balance_found:
        pics = astro["balance_pics"]
    else:
        pics = astro["not_balance_pics"]
    pic_key = selectedID
    if not selectedID in pics: # if the key does not exist, assume the default (any balance)
        pic_key = 'default'
    chance = pics[pic_key]["chance"]
    pic = pics[pic_key]["pics"]
    if randint(0, 100) <= chance:
        await bot.say(choice(pic))
    