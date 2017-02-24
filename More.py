import gamelocker
from gamelocker.strings import pretty

APIKEY = "aaa.bbb.ccc"
api = gamelocker.Gamelocker(APIKEY).Vainglory()
def findRole(player):
    roam = 0
    crystal = 0
    weapon = 0
    jungler = 0
    lane = 0
    captain = 0
    roam_ = 0
    weapon_ = 0
    crystal_ = 0
    role = ""
    power = ""
    hero = {}
    try:
        matches = api.matches({"page[limit]": 50, "sort": "createdAt", "filter[playerNames]": player})
    except:
        try:
            matches = gamelocker.Gamelocker(APIKEY).Vainglory(region = "eu").matches({"page[limit]": 50, "filter[playerNames]": player})
        except:
            try:
                matches = gamelocker.Gamelocker(APIKEY).Vainglory(region = "sg").matches({"page[limit]": 50, "filter[playerNames]": player})
            except:
                return("")
    items = {'Crystal': ['Echo', 'Crystal Matrix', 'Frostburn', 'EveOfHarvest', 'Broken Myth', 'Shatterglass', 'Crystal1', 'Heavy Prism', 'Aftershock', 'Void Battery', 'Cogwheel', 'Crystal3', 'Crystal2', 'Steam Battery', 'PiercingShard', 'Clockwork', 'Halcyon Chargers', 'Cooldown1'],
    'Weapon': ['Weapon3', 'BreakingPoint', 'Critical', 'LuckyStrike', 'Tornado Trigger', 'Tension Bow', 'AttackSpeed2', 'MinionsFoot', 'Weapon Blade', 'AttackSpeed1', 'BookOfEulogies', 'Heavy Steel', 'Six Sins', 'Armor Shredder', 'PoisonedShiv', 'PiercingSpear', 'Serpent Mask'],
    'Roam': ['Fountain of Renewal', 'Flaregun', 'War Treads', 'Flare', 'Scout Trap', 'Atlas Pauldron', 'Crucible', 'Stormcrown', 'Shiversteel', 'Contraption', 'StormguardBanner', 'NullwaveGauntlet', 'Dragonblood Contract', 'IronguardContract', 'Lifewell'],
    'More': ['Armor2', 'Boots2', 'Reflex Block', 'Armor3', 'Boots3', 'Boots1', 'SlumberingHusk', 'Light Armor', 'Shield 2', 'Mulled Wine', 'Light Shield', 'Health2']
    }
    l = []
    for p in matches:
        crystal = 0
        roam = 0
        weapon = 0
        #match.rosters[team].participants[player].player.name
        #i.rosters[1].participants[1].stats
        for j in p.rosters:
            for k in j.participants:
                if k.player.name == player:
                    if k.stats["farm"] <= 20:
                        roam += 7
                    for i in k.stats["items"]:
                        if i in items["Crystal"]:
                            crystal+=1
                        elif i in items["Weapon"]:
                            weapon += 1
                        elif i in items["Roam"]:
                            roam +=1
                        if k.stats["assists"] > k.stats["kills"]:
                            roam += 1
                        if k.stats["kills"] > k.stats["assists"]:
                            crystal += 2
                            weapon += 2
                    if pretty(k.actor) in hero:
                        hero[pretty(k.actor)] +=1
                    else:
                        hero[pretty(k.actor)] = 0
                    #Jungle minions killed to find roam jungl and lane
        if roam > weapon and roam > crystal:
            captain +=1
            roam_ += 1
        elif k.stats["jungleKills"] > k.stats["nonJungleMinionKills"]:
            jungler += 1
        elif k.stats["jungleKills"] < k.stats["nonJungleMinionKills"]:
            lane += 1
        if weapon > roam and weapon > crystal:
            weapon_ += 1
        if crystal > roam and crystal > weapon:
            crystal_ += 1
    if weapon_ > crystal_ and weapon_ > roam_:
        power = "WP"

    if crystal_ > weapon_ and crystal_ > roam_:
        power = "CP"

    if roam_ > crystal_ and roam_ > weapon_:
        power = "Utility"

    if lane > jungler and lane > captain:
        role = "Carry"

    if jungler > lane and jungler > captain:
        role = "Jungler"

    if captain > jungler and captain > lane:
        role = "Captain"

    stuff = {
    "Role": role,
    "Power": power,
    "Hero": max(hero, key=hero.get)
    }
    return(stuff)
print(findRole("IraqiZorro"))
