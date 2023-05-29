import asyncio
import discord # Подключаем библиотеку
from discord.ext import commands
import config
import os, re


intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents) 
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"{bot.user} Заглядывает в будку!")
    
@bot.event
async def on_member_join(member):
    await dm_about_roles(member)

@bot.event
async def on_message(message):
    print("Saw a message...")

    if message.author == bot.user:
        return
    
    if isinstance(message.channel, discord.channel.DMChannel):
        await assign_roles(message)
        return

    if message.content.startswith("!roles"):
        await dm_about_roles(message.author)
        
    elif message.content.startswith("!serverid"):
        await message.channel.send(message.channel.guild.id)


async def assign_roles(message):
    print("Assigning roles...")

    languages = set(re.findall("python|javascript|rust|go|c\+\+", message.content, re.IGNORECASE))
    
    language_emojis = set(re.findall("\U0001F40D|\U0001F578|\U0001F980|\U0001F439|\U0001F409", message.content))

    for emoji in language_emojis:
        {
            "\U0001F40D": lambda: languages.add("python"),
            "\U0001F578": lambda: languages.add("javascript"),
            "\U0001F980": lambda: languages.add("rust"),
            "\U0001F439": lambda: languages.add("go"),
            "\U0001F409": lambda: languages.add("c++")
        }[emoji]()
        
    if languages:
        server = bot.get_guild("1112196389619904525")

        new_roles = set([discord.utils.get(server.roles, name=language.lower()) for language in languages])
        member = await server.fetch_member(message.author.id)
        current_roles = set(member.roles)
        roles_to_add = new_roles.difference(current_roles)
        roles_to_remove = new_roles.intersection(current_roles)
                    
        try:
            await member.add_roles(*roles_to_add, reason="Roles assigned by WelcomeBot.")
            await member.remove_roles(*roles_to_remove, reason="Roles revoked by WelcomeBot.")
        except Exception as e:
            print(e)
            await message.channel.send("Error assigning/removing roles.")
        else:
            if roles_to_add:
                await message.channel.send(f"You've been assigned the following role{'s' if len(roles_to_add) > 1 else ''} on {server.name}: { ', '.join([role.name for role in roles_to_add]) }")
            if roles_to_remove:
                await message.channel.send(f"You've lost the following role{'s' if len(roles_to_remove) > 1 else ''} on {server.name}: { ', '.join([role.name for role in roles_to_remove]) }")
    else:
        await message.channel.send("No supported languages were found in your message.")

async def dm_about_roles(member):
    print(f"DMing {member.name}...")
    await member.send(
        f"""Hi {member.name}, welcome to {member.guild.name}!

Which of these languages do you use:

* Python (🐍)
* JavaScript (🕸️)
* Rust (🦀)
* Go (🐹)
* C++ (🐉)

Reply to this message with one or more of the language names or emojis above so I can assign you the right roles on our server.

Reply with the name or emoji of a language you're currently using and want to stop and I'll remove that role for you.
"""
    )
    
@bot.command()
async def babushka(ctx):
    author_mention = ctx.author.mention
    await ctx.send(f'{author_mention} barya')

    
#Удаление сообщений    
@bot.command()
async def clear(ctx, count:int):
    await ctx.channel.purge(limit=count+1)
    await ctx.send(f"Баря сьела {count} сообщений")

@bot.command()
async def help(ctx):
    await ctx.send("Подсказки:\n1)В будку не лезть нахуй\n2)Очистка сообщений: !clear 'кол-во'")



bot.run(os.environ.get("TOKEN"))




# @bot.command()
# async def join(ctx):
#     channel = ctx.message.author.voice.channel
#     await channel.connect()

# async def on_message(ctx):
#     if ctx.author != bot.user:
#         await ctx.reply(ctx.content)

# @bot.event
# async def on_ready():
#     print(f'Logged in as {bot.user}')

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return



#TOKEN="MTExMjE4NzUwNjg1NTc4ODY1OA.Gf8Bqj.YNxfuSTRIBvNGxheI3XqyWD8HQwrcMXLoA2WqQ"


