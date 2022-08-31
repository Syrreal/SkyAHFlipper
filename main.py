import asyncio
import json
from sortedcontainers import SortedKeyList
import requests
import logging
import discord
from discord.ext import tasks

# Put discord bot token here!!!
TOKEN = ""

logging.basicConfig(level=logging.WARNING)

intents = discord.Intents(messages=True)

enchant_dict = {
    # Sword
    "Bane of Arthropods VI": 0, "Bane of Arthropods VII": 0,
    "Cleave VI": 0,
    "Critical VI": 0, "Critical VII": 0,
    "Cubism VI": 0,
    "Dragon Hunter I": 0, "Dragon Hunter II": 0, "Dragon Hunter III": 0, "Dragon Hunter IV": 0, "Dragon Hunter V": 0,
    "Ender Slayer VI": 0, "Ender Slayer VII": 0,
    "Execute VI": 0,
    "Experience IV": 0,
    "Fire Aspect III": 0,
    "First Strike V": 0,
    "Giant Killer VI": 0, "Giant Killer VII": 0,
    "Lethality VI": 0,
    "Life Steal IV": 0, "Life Steal V": 0,
    "Looting IV": 0, "Looting V": 0,
    "Luck VI": 0, "Luck VII": 0,
    "Prosecute VI": 0,
    "Scavenger IV": 0, "Scavenger V": 0,
    "Sharpness VI": 0, "Sharpness VII": 0,
    "Smite VI": 0, "Smite VII": 25000000,
    "Smoldering I": 0, "Smoldering II": 0, "Smoldering III": 0, "Smoldering IV": 0, "Smoldering V": 0,
    "Syphon IV": 0, "Syphon V": 0,
    "Thunderbolt VI": 0, "Thunderbolt VII": 0,
    "Thunderlord VI": 0, "Thunderlord VII": 0,
    "Titan Killer VI": 0, "Titan Killer VII": 0,
    "Vampirism VI": 0,
    "Venomous VI": 0,
    "Vicious III": 0, "Vicious IV": 0, "Vicious V": 0,
    # Bow
    "Chance IV": 0, "Chance V": 0,
    "Infinite Quiver VI": 0, "Infinite Quiver VII": 0, "Infinite Quiver VIII": 0, "Infinite Quiver IX": 0, "Infinite Quiver X": 0,
    "Overload I": 0, "Overload II": 0, "Overload III": 0, "Overload IV": 0, "Overload V": 0,
    "Power VI": 0, "Power VII": 0,
    "Snipe IV": 0,
    # Armor
    "Big Brain III": 0, "Big Brain IV": 0, "Big Brain V": 0,
    "Blast Protection VI": 0, "Blast Protection VII": 0,
    "Counter-Strike V": 0,
    "Feather Falling VI": 0, "Feather Falling VII": 0, "Feather Falling VIII": 0, "Feather Falling IX": 0,
    "Feather Falling X": 0, "Feather Falling XX": 0,
    "Ferocious Mana I": 0, "Ferocious Mana II": 0, "Ferocious Mana III": 0, "Ferocious Mana IV": 0,
    "Ferocious Mana V": 0, "Ferocious Mana VI": 0, "Ferocious Mana VII": 0, "Ferocious Mana VIII": 0,
    "Ferocious Mana IX": 0, "Ferocious Mana X": 0,
    "Fire Protection VI": 0, "Fire Protection VII": 0,
    "Growth VI": 0, "Growth VII": 0,
    "Hardened Mana I": 0, "Hardened Mana II": 0, "Hardened Mana III": 0, "Hardened Mana IV": 0, "Hardened Mana V": 0,
    "Hardened Mana VI": 0, "Hardened Mana VII": 0, "Hardened Mana VIII": 0, "Hardened Mana IX": 0, "Hardened Mana X": 0,
    "Mana Vampire I": 0, "Mana Vampire II": 0, "Mana Vampire III": 0, "Mana Vampire IV": 0, "Mana Vampire V": 0,
    "Mana Vampire VI": 0, "Mana Vampire VII": 0, "Mana Vampire VIII": 0, "Mana Vampire IX": 0, "Mana Vampire X": 0,
    "Projectile Protection VI": 0, "Projectile Protection VII": 0,
    "Protection VI": 0, "Protection VII": 0,
    "Rejuvenate I": 0, "Rejuvenate II": 0, "Rejuvenate III": 0, "Rejuvenate IV": 0, "Rejuvenate V": 0,
    "Strong Mana I": 0, "Strong Mana II": 0, "Strong Mana III": 0, "Strong Mana IV": 0, "Strong Mana V": 0,
    "Strong Mana VI": 0, "Strong Mana VII": 0, "Strong Mana VIII": 0, "Strong Mana IX": 0, "Strong Mana X": 0,
    "Respite I": 0, "Respite II": 0, "Respite III": 0, "Respite IV": 0, "Respite V": 0,
    "True Protection I": 900000,
    "Smarty Pants I": 0, "Smarty Pants II": 0, "Smarty Pants III": 0, "Smarty Pants IV": 0, "Smarty Pants V": 0,
    "Sugar Rush I": 0, "Sugar Rush II": 0, "Sugar Rush III": 0,
    # Tool
    "Cultivating I": 0, "Cultivating II": 0, "Cultivating III": 0, "Cultivating IV": 0, "Cultivating V": 0,
    "Cultivating VI": 0, "Cultivating VII": 0, "Cultivating VIII": 0, "Cultivating IX": 0, "Cultivating X": 0,
    "Compact I": 0, "Compact II": 0, "Compact III": 0, "Compact IV": 0, "Compact V": 0,
    "Compact VI": 0, "Compact VII": 0, "Compact VIII": 0, "Compact IX": 0, "Compact X": 0,
    "Delicate": 0,
    "Efficiency VI": 0, "Efficiency VII": 0, "Efficiency VIII": 0, "Efficiency IX": 0, "Efficiency X": 0,
    "Fortune IV": 0,
    "Harvesting VI": 0,
    "Pristine I": 0, "Pristine II": 0, "Pristine III": 0, "Pristine IV": 0, "Pristine V": 0,
    "Rainbow II": 0,
    "Replenish I": 0,
    "Turbo-Wheat I": 0, "Turbo-Wheat II": 0, "Turbo-Wheat III": 0, "Turbo-Wheat IV": 0, "Turbo-Wheat V": 0,
    "Turbo-Carrot I": 0, "Turbo-Carrot II": 0, "Turbo-Carrot III": 0, "Turbo-Carrot IV": 0, "Turbo-Carrot V": 0,
    "Turbo-Potato I": 0, "Turbo-Potato II": 0, "Turbo-Potato III": 0, "Turbo-Potato IV": 0, "Turbo-Potato V": 0,
    "Turbo-Pumpkin I": 0, "Turbo-Pumpkin II": 0, "Turbo-Pumpkin III": 0, "Turbo-Pumpkin IV": 0, "Turbo-Pumpkin V": 0,
    "Turbo-Melon I": 0, "Turbo-Melon II": 0, "Turbo-Melon III": 0, "Turbo-Melon IV": 0, "Turbo-Melon V": 0,
    "Turbo-Mushrooms I": 0, "Turbo-Mushrooms II": 0, "Turbo-Mushrooms III": 0, "Turbo-Mushrooms IV": 0, "Turbo-Mushrooms V": 0,
    "Turbo-Cocoa I": 0, "Turbo-Cocoa II": 0, "Turbo-Cocoa III": 0, "Turbo-Cocoa IV": 0, "Turbo-Cocoa V": 0,
    "Turbo-Cactus I": 0, "Turbo-Cactus II": 0, "Turbo-Cactus III": 0, "Turbo-Cactus IV": 0, "Turbo-Cactus V": 0,
    "Turbo-Cane I": 0, "Turbo-Cane II": 0, "Turbo-Cane III": 0, "Turbo-Cane IV": 0, "Turbo-Cane V": 0,
    "Turbo-Warts I": 0, "Turbo-Warts II": 0, "Turbo-Warts III": 0, "Turbo-Warts IV": 0, "Turbo-Warts V": 0,
    # Fishing Rod
    "Angler VI": 0,
    "Blessing VI": 0,
    "Caster VI": 0,
    "Charm I": 0, "Charm II": 0, "Charm III": 0, "Charm IV": 0, "Charm V": 0,
    "Corruption I": 0, "Corruption II": 0, "Corruption III": 0, "Corruption IV": 0, "Corruption V": 0,
    "Expertise I": 0, "Expertise II": 0, "Expertise III": 0, "Expertise IV": 0, "Expertise V": 0,
    "Expertise VI": 0, "Expertise VII": 0, "Expertise VIII": 0, "Expertise IX": 0, "Expertise X": 0,
    "Frail VI": 0,
    "Luck of the Sea VI": 0,
    "Lure VI": 0,
}

# TODO: Populate reforge dict and get prices
reforge_dict = {
    # Sword
    "Gentle": 0, "Odd": 0, "Fast": 0, "Fair": 0, "Epic": 0, "Sharp": 0, "Heroic": 0, "Spicy": 0, "Legendary": 0,

    "Dirty": 0, "Fabled": 0, "Suspicious": 0, "Gilded": 0, "Warped": 0, "Withered": 0, "Bulky": 0,
    # Fishing Rod
    "Salty": 0, "Treacherous": 0, "Stiff": 0, "Lucky": 0,
    # Bow
    "Deadly": 0, "Fine": 0, "Grand": 0, "Hasty": 0, "Neat": 0, "Rapid": 0, "Unreal": 0, "Awkward": 0, "Rich": 0,

    "Precise": 0, "Spiritual": 0, "Headstrong": 0,
    # Armor
    "Clean": 0, "Fierce": 0, "Heavy": 0, "Light": 0, "Mythic": 0, "Pure": 0, "Smart": 0, "Titanic": 0, "Wise": 0,

    "Perfect": 0, "Necrotic": 0, "Ancient": 0, "Spiked": 0, "Renowned": 0, "Cubic": 0, "Hyper": 0, "Reinforced": 0,
    "Loving": 0, "Ridiculous": 0, "Empowered": 0, "Giant": 0, "Submerged": 0, "Jaded": 0,
    # Tool
    "Double-Bit": 0, "Lumberjack's": 0, "Great": 0, "Rugged": 0, "Lush": 0, "Green Thumb": 0, "Peasant's": 0,
    "Robust": 0, "Zooming": 0, "Unyielding": 0, "Prospector's": 0, "Excellent": 0, "Sturdy": 0, "Fortunate": 0,

    "Moil": 0, "Toil": 0, "Blessed": 0, "Bountiful": 0, "Magnetic": 0, "Fruitful": 0, "Refined": 0, "Stellar": 0,
    "Mithraic": 0, "Auspicious": 0, "Fleet": 0, "Heated": 0, "Ambered": 0,
    # Equipment
    "Waxed": 0, "Fortified": 0, "Strengthened": 0, "Glistening": 0,
}

# The keywords to exclude when stripping the reforges out of item names
# This is used in addition to the reforge_dict because some items have the same prefix as a reforge
# also used for reforge pricing of those items
duplicate_reforges_dict = {
    "Very": 0,
    "Extremely": 0,
    "Not So": 0,
    "Thicc": 0,
    "Absolutely": 0,
    "Even More": 0,
}

# The full names of the items that have prefixes similar to a reforge
# if an item in this list shows up when querying the API then we use the duplicate_reforges_dict to strip the name
# instead of using the regular reforge dict
reforge_exceptions_list = {
    "Very Wise Dragon Armor",
    "Extremely Heavy Armor",
    "Not So Heavy Armor",
    "Thicc Super Heavy Armor",
    "Absolutely Perfect Armor",
    "Even More Refined Mithril Pickaxe",
    "Even More Refined Titanium Pickaxe"
}

# TODO: Get correct values for 6-10 star items
star_dict = {
    "➊": 10000,
    "❷": 20000,
    "❸": 30000,
    "❹": 40000,
    "❺": 50000,
}

tier_dict = {
    "COMMON": 0,
    "UNCOMMON": 1,
    "RARE": 2,
    "EPIC": 3,
    "LEGENDARY": 4,
    "MYTHIC": 5,
    "DIVINE": 6,
    "SPECIAL": 7,
    "VERY_SPECIAL": 8,
    "SUPREME": 9
}


# Sorted list key
def sort_items(item):
    if isinstance(item, Item):
        name = item.name
        tier = tier_dict[item.tier]
    else:
        name = item[0]
        tier = tier_dict[item[1]]

    return tuple((name, tier))


def name_stripper(name):
    stripped_name = ''
    for letter in name:
        if letter.isascii():
            stripped_name += letter
    temp_list = []
    if stripped_name in reforge_exceptions_list:
        temp_list = [word for word in stripped_name if word not in duplicate_reforges_dict]
    else:
        temp_list = [word for word in stripped_name if word not in reforge_dict]
    stripped_name = ' '.join(temp_list)
    return stripped_name


# sleeps for half a second to guarantee only 120 api calls per minute
# used in bot startup and bi-hourly full AH parsing
async def prevent_api_spam():
    await asyncio.sleep(0.5)


# TODO: Add dynamic pricing of enchants by checking if the enchanted book contains ONLY a single enchant
#       in the enchant_dict
async def full_parse(api_link):
    response = requests.get(api_link)
    if response.status_code == 200:
        content = json.loads(response.content)
        content = content["auctions"]
        for element in content:
            element_in_list = False
            if element['bin']:
                if element['item_name'] == "Enchanted Book" or "Pet" in element["item_lore"]:
                    continue
                name = name_stripper(element['item_name'])
                tier = element["tier"]
                if len(Flipper.auction_list):
                    if (name, tier) in Flipper.auction_list:
                        element_in_list = True
                        index = Flipper.auction_list.index((name, tier))
                        item = Flipper.auction_list[index]
                        item.occurrence(element["starting_bid"])
                        if item.lowest_price > element["starting_bid"]:
                            item.lowest_price = element["starting_bid"]
                    if not element_in_list:
                        item = Item(name, tier)
                        Flipper.auction_list.add(item)
                        item.occurrence(element["starting_bid"])
                        item.lowest_price = element["starting_bid"]
                else:
                    item = Item(name, tier)
                    Flipper.auction_list.add(item)
                    item.occurrence(element["starting_bid"])
                    item.lowest_price = element["starting_bid"]


# Full parse clears the auction list and rebuilds it from the currently available auctions
# ALWAYS CALL WITH THE FLIPPER LOCK
async def run_full_parse():
    """
    Always call this function with an async.lock !!
    """
    print("Starting full AH parse")
    # Start on page 2 to avoid potential undercuts during full parse
    # this is important to get an accurate lowest_price
    page = 2
    total_pages = 100
    failures = 0
    while page < total_pages:
        # if we fail to get a response from the initial query in 20 seconds, abort
        if failures > 9:
            print("Failed to query api -- aborting")
            return
        if failures:
            # if we fail to get a response from the initial query, wait 2 seconds before trying again
            await asyncio.sleep(2)
        if page == 2:
            response = requests.get("https://api.hypixel.net/skyblock/auctions?page=0")
            if response.status_code == 200:
                content = json.loads(response.content)
                total_pages = int(content["totalPages"]) - 1
                # Wait until we get a successful response to clear the auction_list so that we don't throw away our
                # listings if we can't receive a response
                Flipper.auction_list.clear()
                failures = 0
            else:
                print("Failed to get api response in initial query -- retrying")
                failures += 1
                continue
        api_link = f'https://api.hypixel.net/skyblock/auctions?page={page}'
        await asyncio.gather(full_parse(api_link), prevent_api_spam())
        page += 1


# NOTE: avg_price is not currently used but still exists because it's an interesting statistic and may be useful
class Item:
    def __init__(self, name, tier):
        self.name = name
        self.tier = tier
        self.avg_price = None
        self.occurrences = 0
        self.lowest_price = None

    def __eq__(self, other):
        """

        :param other: an Item class object or a tuple of (name, tier)
        :return: bool
        """
        if isinstance(other, Item):
            return self.name == other.name and self.tier == other.tier
        else:
            return self.name == other[0] and self.tier == other[1]

    def __ne__(self, other):
        """

        :param other: an Item class object or a tuple of (name, tier)
        :return: bool
        """
        if isinstance(other, Item):
            return self.name != other.name or self.tier != other.tier
        else:
            return self.name != other[0] or self.tier != other[1]

    def __lt__(self, other):
        """

        :param other: an Item class object or a tuple of (name, tier)
        :return: bool
        """
        if isinstance(other, Item):
            return self.name < other.name and self.tier < other.tier
        else:
            return self.name < other[0] and self.tier < other[1]

    def __gt__(self, other):
        """

        :param other: an Item class object or a tuple of (name, tier)
        :return: bool
        """
        if isinstance(other, Item):
            return self.name > other.name and self.tier > other.tier
        else:
            return self.name > other[0] and self.tier > other[1]

    def __str__(self):
        return f'{self.tier} {self.name}: AvgPrice: {self.avg_price}, LowestPrice: {self.lowest_price}'

    def occurrence(self, price):
        self.occurrences += 1
        if self.avg_price:
            self.avg_price = self.avg_price + ((price - self.avg_price) / self.occurrences)
        else:
            self.avg_price = price


class Flipper(discord.Client):
    # channel_id of the active DM, 0 if bot is inactive
    active_dm = 0
    # queued flips, will finish sending before resetting active dm if bot is stopped
    # this is a list of tuples (Item, actual price, price diff)
    flip_queue = []
    # auction_list stores results from previous api requests
    auction_list = SortedKeyList([], key=sort_items)
    # the epoch time of the last time the auction list was updated, used to avoid erroneous
    last_update = 0

    def __init__(self, **options):
        super().__init__(**options)
        self.lock = asyncio.Lock()
        self.on_start()

    # runs a full AH query before bot is available
    def on_start(self):
        print("Running Initialization Query")
        # the bot is not asynchronous at this point so no lock is required for the run_full_parse function
        asyncio.run(run_full_parse())

    async def on_ready(self):
        print(f'{self.user} is connected')

    # asynchronous function for resetting the active DM
    # this is required to be asynchronous to ensure messages are always sent before the active DM is reset
    # otherwise they will fail and raise an exception
    async def reset_active_dm(self):
        self.active_dm = 0

    @tasks.loop(minutes=30)
    async def reset_ah_list(self):
        async with self.lock:
            await run_full_parse()

    # Sends a message to the active dm containing flip data, prints all flips in the queue
    # Finishes printing and clears the queue after flip_loop is stopped and before the active dm is reset
    @tasks.loop()
    async def flip_printer(self):
        for item in self.flip_queue:
            #                       flip queue tuple -- (Item, actual price, price diff)
            await self.active_dm.send(f'```Potential flip --- {item[0].tier} {item[0].name}\n'
                                      # Actual item cost
                                      f'Price: {item[1]}\n'
                                      # Projected item cost is what the bot determines the item should sell at
                                      # this may not be higher than the lowest recorded price (undercutting)
                                      f'Projected selling price: {item[2] + item[1]}'
                                      # Profit = price diff - tax
                                      # tax is 1% for items below 1mil and 2% for items over
                                      f'Profit: {(item[2] + item[1]) - (item[1] * .02 if item[1] >= 1000000 else item[1] * .01)}```')
            self.flip_queue.remove(item)

    def calculate_price(self, element):
        price = 0
        has_dupe_reforge = False
        for enchant in enchant_dict:
            if enchant in element["item_lore"]:
                price += enchant_dict[enchant]
        for dupe in duplicate_reforges_dict:
            if dupe in element["item_name"]:
                price += duplicate_reforges_dict[dupe]
                has_dupe_reforge = True
        if not has_dupe_reforge:
            for reforge in reforge_dict:
                if reforge in element["item_name"]:
                    price += reforge_dict[reforge]
        star = element["item_name"].count('✪')
        if star == 5:
            for starcount in star_dict:
                if starcount in element["item_name"]:
                    price += star_dict[starcount]
        return price

    @tasks.loop(seconds=1)
    async def flip_loop(self, minimum, maximum):
        async with self.lock:
            response = requests.get('https://api.hypixel.net/skyblock/auctions')
            if response.status_code == 200:
                content = json.loads(response.content)
                if self.last_update == content["lastUpdated"]:
                    return
                else:
                    self.last_update = content["lastUpdated"]
                content = content["auctions"]
                for element in content:
                    if element['bin']:
                        if element['item_name'] != "Enchanted Book" and "Pet" not in element["item_lore"]:
                            name = name_stripper(element["item_name"])
                            tier = element["tier"]
                            if (name, tier) not in self.auction_list:
                                item = Item(name, tier)
                                self.auction_list.append(item)
                                item.occurrence(element["starting_bid"])
                                await self.active_dm.send('```'
                                                          f'{item.tier} {item.name} is a rare item on the AH!\n'
                                                          f'A new bid for {element["starting_bid"]} was just created'
                                                          '```')
                                continue
                            index = self.auction_list.index((name, tier))
                            item = self.auction_list[index]
                            item.occurrence(element["starting_bid"])
                            # projected item price =
                            # lowest item price + price of enchants + price of reforge + price of dungeon stars > 5
                            projected_price = self.calculate_price(element) + item.lowest_price
                            # diff = projected item price - actual item price
                            # if the item has no enchants or reforge; diff = starting price - lowest price
                            if projected_price:
                                diff = projected_price - element["starting_bid"]
                            else:
                                diff = element["starting_bid"] - item.lowest_price
                            if maximum and minimum <= diff <= maximum:
                                self.flip_queue.append((item, element["starting_bid"], diff))
                                continue
                            elif minimum <= diff:
                                self.flip_queue.append((item, element["starting_bid"], diff))
                                continue
                            if item.occurrences <= 10:
                                await self.active_dm.send('```'
                                                          f'{item.tier} {item.name} is a rare item on the AH!\n'
                                                          f'A new bid for {element["starting_bid"]} was just created'
                                                          '```')

    # determines filters used for sending potential AH flips
    # times out if min and max aren't set within 1 minute
    # if it times out the active dm is set back to 0
    async def start_flip_spam(self):
        reply_msg = await self.active_dm.send("```"
                                              "Please reply to this message with a minimum and maximum profit "
                                              "margin\n\n"
                                              "Use this format: \"<min>:<max>\"\n"
                                              "For no max boundary use 0"
                                              "```"
                                              "_Bot will timeout after 1 minute_")

        def check(message):
            try:
                return message.channel == self.active_dm and message.reference.message_id == reply_msg.id
            except AttributeError:
                return False
            else:
                raise

        min_margin = 0
        max_margin = 0
        timed_out = 0
        while not timed_out:
            try:
                msg = await client.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await self.active_dm.send("```"
                                          "Timed out, re-type \"start\" to retry"
                                          "```")
                timed_out = 1
            else:
                margins = msg.content
                margins = margins.replace(" ", "")
                if margins.find(":") != -1:
                    margins = margins.split(":")
                    if margins[0].isdigit() and margins[1].isdigit():
                        margins[0] = int(margins[0])
                        margins[1] = int(margins[1])
                        min_margin = margins[0]
                        max_margin = margins[1]
                        if min_margin < max_margin:
                            pass
                        elif max_margin == 0:
                            pass
                        else:
                            await msg.reply("```"
                                            "Max value is smaller than the minimum!"
                                            "```")
                            continue
                else:
                    continue
                await msg.reply("```"
                                f'Bot will begin flip with a minimum profit margin of {min_margin}'
                                f' and a maximum of {max_margin}'
                                "```")

                break

        if not timed_out:
            self.flip_loop.start(min_margin, max_margin)
            self.flip_printer.start()
            print('Starting flip loop -----')
            pass
        else:
            await self.reset_active_dm()
        return

    @flip_printer.after_loop
    async def printer_cleanup(self):
        if self.flip_printer.is_being_cancelled() and len(self.flip_queue) != 0:
            await self.flip_printer()

    @flip_loop.after_loop
    async def clear_data(self):
        self.flip_printer.stop()
        self.auction_list.clear()
        return 1

    async def stop_loop(self):
        self.flip_loop.stop()
        return 1

    # stops request and spam loops, spam loop will finish clearing the queue before stopping
    async def stop_flip_spam(self):
        await self.active_dm.send("```"
                                  "Flushing spam queue before stopping"
                                  "```")
        await self.stop_loop()
        await self.clear_data()
        await self.active_dm.send("```"
                                  "Bot is now inactive"
                                  "```")
        await self.reset_active_dm()
        return

    # checks for a start or stop message and confirms that the user sending it is allowed to
    async def on_message(self, message):
        if message.channel.type == discord.ChannelType.private:
            if message.content == 'start':
                if self.active_dm == 0:
                    self.active_dm = message.channel
                    await self.start_flip_spam()
                else:
                    await message.channel.send('Bot is already in use!')
            if message.content == 'stop':
                if message.channel == self.active_dm:
                    await self.stop_flip_spam()
                else:
                    await message.channel.send("You can not stop what has not begun :upside_down:")
        return


if __name__ == '__main__':
    client = Flipper()
    client.run(TOKEN)
