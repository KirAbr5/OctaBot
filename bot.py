import discord
from discord.ext import commands

TOKEN = ""
PREFIX = ">"
intents = discord.Intents().all()

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.voice_states = True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def hello(ctx):
    await ctx.reply("Привет, друг!\nЧем могу помочь?")
    await ctx.send("Вот все мои команды: \n ・ >hello - все команды. \n ・ >count - счет. \n ・ >ban - бан участника. \n ・ >unban - разбан участника. \n ・ >mute - замутить участника. \n ・ >unmute - размутить участника. \n ・ >kick - кик с сервера. \n ・ >echo - эхо вашего сообщения.")


@commands.has_permissions(ban_members=True)
@bot.command()
async def ban(ctx, user: discord.Member, *, reason="причины не дано"):
        await user.ban(reason=reason)
        ban = discord.Embed(title=f":boom: Забанил {user.name}!", description=f"По причине: {reason}\nОт: {ctx.author.mention}")
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    guild = ctx.guild
    try:
        user = await bot.fetch_user(user_id)
        await guild.unban(user)
        await ctx.send(f'Пользователь {user.name} был разбанен.')
    except discord.NotFound:
        await ctx.send(f'Пользователь с ID {user_id} не найден в бан-листе.')
    except discord.Forbidden:
        await ctx.send('У меня нет прав на разбан этого пользователя.')
    except discord.HTTPException:
        await ctx.send('Произошла ошибка при попытке разбана пользователя.')


@commands.has_permissions(administrator=True)
@bot.command()
async def kick(ctx, user: discord.Member, *, reason="причины не дано"):
        await user.kick(reason=reason)
        kick = discord.Embed(title=f":boom: Кикнул {user.name}!", description=f"По причине: {reason}\nОт: {ctx.author.mention}")
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)


@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mute_role = discord.utils.get(guild.roles, name="Muted")
    if not mute_role:
        mute_role = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False, add_reactions=False)
    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f"{member.mention} был замучен по причине: {reason}")


@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if mute_role in member.roles:
        await member.remove_roles(mute_role)
        await ctx.send(f"{member.mention} был размучен.")
    else:
        await ctx.send(f"{member.mention} не был замучен.")


@bot.command()
async def echo(ctx, *args):
    await ctx.send(args)


@bot.command()
async def count(ctx, a, b, c):
    if b == "+":
        await ctx.send(int(a) + int(c))
    if b == "-":
        await ctx.send(int(a) - int(c))
    if b == "*":
        await ctx.send(int(a) * int(c))
    if b == "/":
        await ctx.send(int(a) / int(c))
    if b == "**":
        await ctx.send(int(a) ** int(c))


bot.run(TOKEN)
