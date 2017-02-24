import gamelocker
from gamelocker.strings import pretty
import discord

APIKEY = "aaa.bbb.ccc"
api = gamelocker.Gamelocker(APIKEY).Vainglory()

def getMatches(name):
    try:
        m = api.matches({"page[limit]": 50, "sort": "createdAt", "filter[playerNames]": name})
    except:
        try:
            m = gamelocker.Gamelocker(APIKEY).Vainglory(region = "eu").matches({"page[limit]": 50, "sort": "createdAt", "filter[playerNames]": name})
        except:
            try:
                m = gamelocker.Gamelocker(APIKEY).Vainglory(region = "sg").matches({"page[limit]": 50, "sort": "createdAt", "filter[playerNames]": name})
            except:
                return(0)
    matches = []
    for i in m:
        matches.append(i)
    return(matches)
def getMatchInfo(name,index=0):
    if getMatches(name) == 0:
        return(False)
    l = getMatches(name)
    stats = {}
    stats["_blue"] = []
    for j in l[index].rosters:
        for i in j.participants:
            if i.player.name == name:
                stats["_items"] = []
                stats["items"] = ""
                stats["blue"] = ""
                minu,secs =divmod(l[index].duration, 60)
                if len(str(secs)) == 2:
                    stats["duration"] = str(minu) + ":" +str(secs)
                else:
                    stats["duration"] = str(minu) + ":0" +str(secs)
                if i.stats["winner"]:
                    stats["win"] = "Victory"
                    stats["color"] = 0x2fe26e
                else:
                    stats["win"] = "Loss"
                    stats["color"] = 0xe22f2f
                for x in i.stats["items"]:
                    stats["_items"].append(pretty(x))
                for v in stats["_items"]:
                    stats["items"] = stats["items"] + v +", "
                stats["id"] = i.id
                stats["items"] = stats["items"][:-2]
                for b in j.participants:
                    stats["_blue"].append(b.player.name)
                for h in stats["_blue"]:
                    stats["blue"] = stats["blue"] + h +",\n"
            elif i.player.name not in stats["_blue"]:
                stats["_orange"] = []
                stats["orange"] = ""
                for z in j.participants:
                    stats["_orange"].append(z.player.name)
                for f in stats["_orange"]:
                    stats["orange"] = stats["orange"] + f +",\n"
    for j in l[index].rosters:
        for i in j.participants:
            if i.player.name not in stats["_blue"]:
                stats["_orange"] = []
                stats["orange"] = ""
                for z in j.participants:
                    stats["_orange"].append(z.player.name)
                for f in stats["_orange"]:
                    stats["orange"] = stats["orange"] + f +",\n"
                #stats["items"] = stats["items"][:-2] + ". "
    return(stats)
def matchEmbed(name, index = 0):
    if getMatchInfo(name) == 0:
        return(discord.Embed(title= "Could not find data for " + name))
    m = getMatchInfo(name,index)
    em = discord.Embed(title= m["win"],url = "http://vain.gg/#/match/"+m["id"] , description=m["duration"]+"\n"+str(index+1) +" out of " +str(len(getMatches(name))), colour=m["color"])
    em.set_author(name='Vainglory Stats', icon_url="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcREVEEL3vFm3boDZD0aSwSPFtZ2EXJGwiEjsnvXXTluLqXrD0mknNohwA")
    em.add_field(name = "Blue:", value = m["blue"])
    em.add_field(name = "Orange:", value = m["orange"])
    em.add_field(name = "Items:", value = m["items"], inline = False)
    return(em)
getMatchInfo("CullTheMeek")
