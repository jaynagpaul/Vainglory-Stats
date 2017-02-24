import gamelocker
import discord, asyncio
import pickle
from statistics import mean
import More, matches
APIKEY = "aaa.bbb.ccc"
api = gamelocker.Gamelocker(APIKEY).Vainglory()
client = discord.Client()
config = {}
client.cooldowns = dict()
def getID(name):
    try:
        m = api.matches({"page[limit]": 2, "filter[playerNames]": name, "sort": "createdAt"})
        for i in m[0].rosters:
            for j in i.participants:
                if j.player.name == name:
                    return(j.player.id)
    except:
        return("Invalid Name")
def storeConfig():
    # Store data (serialize)
    with open('theconfig.pickle', 'wb') as handle:
        pickle.dump(config, handle, protocol=pickle.HIGHEST_PROTOCOL)
def getConfig():
    global config
    #Load data (deserialize)
    with open('theconfig.pickle', 'rb') as handle:
        config = pickle.load(handle)
def getStats(name):
    try:
        m = api.matches({"page[limit]": 50, "filter[playerNames]": name, "sort": "createdAt"})
    except:
        try:
            m = gamelocker.Gamelocker(APIKEY).Vainglory(region = "eu").matches({"page[limit]": 50, "filter[playerNames]": name, "sort": "createdAt"})
        except:
            try:
                m = gamelocker.Gamelocker(APIKEY).Vainglory(region = "sg").matches({"page[limit]": 50, "filter[playerNames]": name, "sort": "createdAt"})
            except:
                return("Could not find stats for " + name)
    l = []
    for i in m:
        for j in i.rosters:
            for k in j.participants:
                if k.player.name == name:
                    l.append(k.stats)
    karmalevels ={
    0: "Bad Karma",
    1: "Good Karma",
    2: "Great Karma"
    }
    winpts = 0
    afkpts = 0
    killpts = []
    assistpts = []
    deathpts = []
    farmpts = []
    for i in l:
        if i["winner"]:
            winpts = winpts + 1
    for i in l:
        if i["wentAfk"]:
            afkpts = afkpts + 1
    afkper = str(int(afkpts / len(l)*100))
    winper = str(int(winpts / len(l)*100))
    for i in l:
        killpts.append(i["kills"])
    for i in l:
        assistpts.append(i["assists"])
    for i in l:
        deathpts.append(i["deaths"])
    for i in l:
        farmpts.append(i["farm"])
    farmpts = str(int(mean(farmpts)))
    deathpts = str(int(mean(deathpts)))
    assistpts = str(int(mean(assistpts)))
    killpts = str(int(mean(killpts)))
    return("**"+name + "'s stats:\nLevel:** " + str(l[0]["level"]) + "\n**Wins:** " + str(l[0]["wins"]) +"\n**avgKDA:** " + killpts+ "/" + deathpts + "/" + assistpts + "\n**avgFarm:** "+ farmpts +"\n**Win%:** " + winper + "%\n" + "**AFK%:** " + afkper + "%\n**" + karmalevels[l[0]["karmaLevel"]] +"**" + "\n**Favorite Hero: **" + More.findRole(name)["Hero"] + "\n**Favorite Role: **" + More.findRole(name)["Role"]+ "\n**Favorite Item Path: **"+ More.findRole(name)["Power"])
getConfig()
@client.event #add user
async def on_message(message):
    if message.author == client.user:
        return
    if not message.author in client.cooldowns.keys() or not client.cooldowns[message.author]:
        if message.content.startswith("|"):
            client.cooldowns[message.author] = True
            await asyncio.sleep(20)
    else:
        return
    client.cooldowns[message.author] = False
    if message.content.startswith('|adduser'):
        if len(message.content.split()) == 2:
            global config
            config[message.author.id] = message.content[9:]
            storeConfig()
            await client.send_message(message.channel, "Set "+message.content[9:]+" as your default IGN.")
        else:
            await client.send_message(message.channel, "That doesn't seem like a valid IGN")
    elif message.content.startswith("|stats") and message.author.id in config and len(message.content.split()) == 2:
        await client.send_message(message.channel, getStats(message.content[7:]))
    elif message.content.startswith("|stats") and message.author.id in config:
        await client.send_message(message.channel, getStats(config[message.author.id]))
    elif message.content.startswith("|stats"):
        await client.send_message(message.channel, getStats(message.content[7:]))
    if message.content.startswith('|help'):
        await client.send_message(message.channel, "**Help:**\n**Prefix: **|\n**|adduser: ** Type |adduser to set your default IGN when you type |stats so you aren't required to enter in your IGN each time.\n**|stats: **|stats can be used to find stats for your default IGN or any IGN specified after.\n**|matches:** Use |matches to view your previous 50 matches, type your IGN then the match number you wish to view [1-50]. \n**Suggestions: **To share suggestions message me on twitter: @SpiesWithin.\n**Bot Link: ** https://discordapp.com/oauth2/authorize?&client_id=275343240968798208&scope=bot")
    if message.content.startswith('|specialtoolonly'):
        await client.change_presence(game=discord.Game(name='Type |help to check out all the commands!'))
        await client.send_message(message.channel, str(len((client.servers))))
    if message.content.startswith('|matches') and message.author.id in config and len(message.content.split()) == 3:
        await client.send_message(message.channel, content = " ", embed = matches.matchEmbed(name = message.content[9:].split()[0], index = int(message.content[9:].split()[1])-1))
    elif message.content.startswith('|matches') and message.author.id in config and len(message.content.split()) == 2:
        await client.send_message(message.channel, content = " ", embed = matches.matchEmbed(config[message.author.id], int(message.content[9:])-1))
    elif message.content.startswith('|matches') and message.author.id in config:
        await client.send_message(message.channel, content = " ", embed = matches.matchEmbed(config[message.author.id]))
    elif message.content.startswith('|matches') and len(message.content.split()) == 3:
        await client.send_message(message.channel, content = " ", embed = matches.matchEmbed(name = message.content[9:].split()[0], index = int(message.content[9:].split()[1])-1))

@client.event #ready message
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.run(YOUR_TOKEN_HERE)
