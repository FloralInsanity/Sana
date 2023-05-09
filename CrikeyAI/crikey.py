# crikey.py

# IMPORT THE OS MODULE.
import os

# FOR TEXT FILES
import json

# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord

# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD = os.getenv('DISCORD_GUILD')

# CREATES A NEW BOT OBJECT WITH A SPECIFIED PREFIX. IT CAN BE WHATEVER YOU WANT IT TO BE.
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

# create a dictionary to store the currency balances
currency = {}
# create a dictionary to store the inventory items
inventory = {"796108491944886352" : {"teddy" : 1, "hot water bottle" : 2}, "381199173183340564" : {"coffee" : 1}}
# create a dictionary to store the shop items and their prices
shop = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
    guild = bot.get_guild(1076982138999685251)
    channel = bot.get_channel(1076982139641409621) 
    await channel.send(f'Say hi to my new friend {member.mention} and welcome them to Tech Guild! \n{member.mention}, please introduce yourself and have a grand time!')
    role = discord.utils.get(guild.roles, id=1078593910449913859)
    await member.add_roles(role)
    currency[member.id] = 0
    inventory[member.id] = {}

@bot.command(name="help")
async def help(ctx):
    #await ctx.channel.send("```help - get help on the commands list!\nping - recieve message pong!```")
    embed = discord.Embed(title="Help", description="", color=0xEBFF11)
    embed.add_field(name="ping - replies \'pong'", value="", inline=False)
    channel = bot.get_channel(ctx.channel.id)
    await channel.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    embed = discord.Embed(title="", description="", color=0xEBFF11)
    embed.add_field(name="", value="pong", inline=True)
    channel = bot.get_channel(ctx.channel.id)
    await channel.send(embed=embed)

@bot.command(name="rules")
async def rules(ctx, *, number = None, post = None):
    embed = discord.Embed(title=f'Rule {number}', description="", color=0xFF0000)
    embed.add_field(name=message.content, value="{}".format(post), inline=False)
    channel = bot.get_channel(1076982139641409617)
    await channel.send(embed=embed)

@bot.command(name="resources")
async def resources(ctx, *, post = None):
    channel = bot.get_channel(1076982139641409619)
    await channel.send(post)

@bot.command(name="announcements")
async def announcements(ctx, *, post = None):
    channel = bot.get_channel(1077344251190444033)
    await channel.send(post)

global logging_channel
logging_channel = 1078610446791221268

@bot.event
async def on_message_delete(message):
    embed = discord.Embed(title="{} deleted a message".format(message.author),
        description="", color=0xFF0000)
    embed.add_field(name=message.content, value="Deleted in the #{} channel".format(message.channel),
        inline=True)
    channel = bot.get_channel(logging_channel)
    await channel.send(embed=embed)

@bot.event
async def on_message_edit(message_before, message_after):
    embed = discord.Embed(title="{} edited a message".format(message_before.author),
        description="", color=0x0000ff)
    embed.add_field(name=message_before.content, value="Before edit", inline=True)
    embed.add_field(name=message_after.content, value="After edit", inline=True)
    channel = bot.get_channel(logging_channel)
    await channel.send(embed=embed)

with open("blacklist.txt") as file: # blacklist.txt contains one phrase per line
    bad_words = [bad_word.strip().lower() for bad_word in file.readlines()]

@bot.event
async def on_message(message):
    message_content = message.content.strip().lower()
    if any(bad_word in message_content for bad_word in bad_words):
        await message.channel.send("{}, can't say that around here chum!".format(message.author.mention))
        await message.delete()
    guild = message.guild
    if not guild:
        embed = discord.Embed(title='{}'.format(message.author), description="", color=0x11FF60)
        embed.add_field(name='Message:', value="{}".format(message.content), inline=False)
        channel = bot.get_channel(1079121876850323559)
        await channel.send(embed=embed)
    #Overriding the default provided on_message forbids any extra commands from running. Fix:
    await bot.process_commands(message)

# command to check inventory of all users
@bot.command(name="inventory_all")
@commands.has_permissions(administrator = True)
async def inventory_all(ctx):
    # create an empty list to store the balance information for each user
    inventory_info = []
    # loop through all members in the server and get their balance
    for member in ctx.guild.members:
        # check if the member is a bot
        if member.bot:
            continue
        with open('inventory.txt', 'r+') as file:
            lines = file.readlines()
            file.seek(0)  # Reset the file pointer to the beginning
            for line in lines:
                inventory_info.append(f"{member}: {line}")
    # join the balance information into a single string and send it as a message
    await ctx.send("\n".join(inventory_info))

@bot.command(name='give')
async def give(ctx, item_name: str):
    # Get the user's ID and username
    user_id = str(ctx.author.id)
    username = str(ctx.author.name)
    # Load the inventory data from the JSON file
    if os.path.exists('inventory.txt'):
        with open('inventory.txt', 'r') as f:
            inventory_data = json.load(f)
    else:
        inventory_data = {}
    # Check if the user has an inventory
    if user_id in inventory_data:
        inventory = inventory_data[user_id]
    else:
        inventory = {}
        inventory_data[user_id] = inventory
    # Add the item to the user's inventory
    if item_name in inventory:
        inventory[item_name] += 1
    else:
        inventory[item_name] = 1
    # Save the updated inventory data to the JSON file
    with open('inventory.txt', 'w') as f:
        json.dump(inventory_data, f)
    # Send a message to confirm that the item was added to the user's inventory
    await ctx.send(f"{username}, {item_name} has been added to your inventory!")
    
@bot.command(name="test")
async def test(ctx):
    found = False
    with open('inventory.txt', 'r+') as file:
        lines = file.readlines()
        file.seek(0)  # Reset the file pointer to the beginning
        for line in lines:
            if line.startswith(str(ctx.author.id)):
                found = True
                parts = line.strip().split(', ')
                num_parts = len(parts)
                embed = discord.Embed(title="Inventory", color=discord.Color.blue())
                for i in range(num_parts):
                    if i == 0:
                        continue
                    else:
                        field_name = str(i)
                        quantity = parts[i]
                        embed.add_field(name=field_name, value=quantity, inline=True)
                await ctx.send(embed=embed)
                break
        else:  # Executed if the loop completes without encountering a 'break'
            new_data = f"{ctx.author.id}, a welcome sticker\n"
            file.write(new_data)
            file.flush()  # Save the changes to the file
            await ctx.send("No inventory found - a new one is created! Retry the command to continue!")

"""
@bot.command(name="test")
async def test(ctx):
    found = False
    with open('inventory.txt', 'r') as file:
        for line in file:
            if line.startswith(str(ctx.author.id)):
                #await ctx.send(line.strip())
                parts = line.split(', ')  # Split the line using a semicolon as the delimiter
                num_parts = len(parts)  # Count the number of parts
                # Create an embed
                embed = discord.Embed(title="Inventory", color=discord.Color.blue())
                # Add fields to the embed
                for i in range(num_parts):
                    if i == 0:
                        continue  # Skip the first part (ID)
                    else:
                        field_name = str(i)
                        quantity = parts[i]
                        embed.add_field(name=field_name, value=quantity, inline=True)
                # Send the embed to the channel
                await ctx.send(embed=embed)
                found = True
                break
    if not found:
        # Create new inventory data
        new_data = f"{ctx.author.id}, a welcome sticker\n"
        inventory_data.append(new_data)
        # Write new data to the text file
        with open('inventory.txt', 'a') as file:
            file.write(new_data)
        await ctx.send("No inventory found - a new one is created! Retry the command to continue!")
"""

global ban_channel
ban_channel = 1078708113588375572

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You never passed in all the requirements kiddo :rolling_eyes:')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command :angry:")

@bot.command(name="ban")
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    guild = bot.get_guild(1076982138999685251)
    role = discord.utils.get(guild.roles, id=1076990530182975618)
    if (role in member.roles):
        await ctx.send('Can\'t ban that person!')
        return
    await member.ban(reason = reason)
    await ctx.send(f"{member.mention} has been banned!")
    embed = discord.Embed(title='Banned.. Forever?', description="", color=0x2d9ad4)
    embed.add_field(name='Member: {}'.format(member), value="{}, the ban hammer has been cast upon you!".format(member.mention), inline=False)
    embed.add_field(name='Mod: {}'.format(ctx.author), value="{}'s reason: {}".format(ctx.author.mention, reason), inline=False)
    channel = bot.get_channel(ban_channel)
    await channel.send(embed=embed)

@bot.command(name="unban")
@commands.has_permissions(administrator = True)
async def unban(ctx, user : discord.User, *, reason = None):
    #if (role in member.roles):
    #    await ctx.send('Can\'t ban that person!')
    #    return
    await ctx.guild.unban(user)
    await ctx.send(f"{user.mention} has been unbanned!")
    embed = discord.Embed(title='Unbanned.. For Now?', description="", color=0x00ff00)
    embed.add_field(name='Member: {}'.format(user), value="{}, you have been forgiven for your sins!".format(user.mention), inline=False)
    embed.add_field(name='Mod: {}'.format(ctx.author), value="{}'s reason: {}".format(ctx.author.mention, reason), inline=False)
    channel = bot.get_channel(ban_channel)
    await channel.send(embed=embed)

# command to give coins to a user
@bot.command(name="give")
@commands.has_permissions(administrator = True)
async def give(ctx, user : discord.User, amount: int):
    # add the currency to the user's balance
    currency[user.id] += amount
    await ctx.send(f"Gave {amount} coins to {user.name}.")
    
# command to reset coins for all users
@bot.command(name="reset_coins")
@commands.has_permissions(administrator = True)
async def reset_coins(ctx):
    # loop through all members in the server and set their balance to 0
    for member in ctx.guild.members:
        currency[member.id] = 0
    await ctx.send("Reset coins for all users.")

# command to reset inventory for all users
@bot.command(name="reset_inventory")
@commands.has_permissions(administrator = True)
async def reset_inventory(ctx):
    # loop through all members in the server and set their inventory to an empty list
    for member in ctx.guild.members:
        inventory[str(member.id)] = {}
    await ctx.send("Reset inventory for all users.")

# command to reset shop
@bot.command(name="reset_shop")
@commands.has_permissions(administrator = True)
async def reset_shop(ctx):
    # sets shop to empty
    shop = []
    await ctx.send("Reset shop")

# command to check balance of all users
@bot.command(name="all_balances")
@commands.has_permissions(administrator = True)
async def all_balances(ctx):
    # create an empty list to store the balance information for each user
    balance_info = []
    # loop through all members in the server and get their balance
    for member in ctx.guild.members:
        # check if the member is a bot
        if member.bot:
            continue
        user_balance = currency.get(member.id, 0)
        balance_info.append(f"{member.mention}: {user_balance} coins")
    # join the balance information into a single string and send it as a message
    await ctx.send("\n".join(balance_info))
     

# command to show the inventory
@bot.command(name="inventory")
async def inventory(ctx):
    user_balance = currency.get(ctx.author.id, 0)
    await ctx.send(f"Your balance is {user_balance} coins.")
    if not inventory.get(ctx.author.id, {}):
        await ctx.send("Your inventory is empty!")
    else:
        inventory_str = "Your inventory:\n"
        for item, quantity in inventory.get(ctx.author.id, {}).items():
            inventory_str += f"{item}: {quantity}\n"
            await ctx.send(inventory_str)
            
# command to add items to the shop
@bot.command()
@commands.has_permissions(administrator = True)
async def add_item(ctx, item: str, price: int):
    # add the item to the shop
    shop[item] = {"price": price, "quantity": 1}
    await ctx.send(f"Added {item} to the shop for {price} coins.")

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN.
bot.run(TOKEN)