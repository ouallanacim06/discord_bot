import discord, os, asyncio
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
def conver_duration(duration: str):
    multiplier = 60 if duration.endswith("m") else 3600
    return int(duration[:-1]) * multiplier
token = os.getenv("tok_name")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)
command_channel_ids = 1241131391501074615
command_channel_id = bot.get_channel(command_channel_ids)
class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.channel_id = None
    @discord.ui.button(label="🎫eopen ticket",style=discord.ButtonStyle.green)
    async def ticket(self, interaction:discord.Interaction, button:discord.ui.Button):
        user = interaction.user
        channel = await user.guild.create_text_channel(f"ticket for {user.name}")
        await channel.set_permissions(user, read_messages=True, send_messages=True)
        await channel.send(f"{user.mention} welcome to the shop an @admin well join you soon")
        everyone = discord.utils.get(user.guild.roles, name="member")
        await channel.set_permissions(everyone,read_messages=False,send_messages=False)
        self.channel_id = channel.id
@bot.event
async def on_ready():
    print("login succful")
    guild = bot.get_guild(803369227167072327)
    channel_com_name = "bot-log"
    channelID = bot.get_channel(1241309467396542468)
    await channelID.send("test")
    view = Menu()
    role = discord.utils.get(guild.roles, name="admin")
    everyone = discord.utils.get(guild.roles, name="member")
    await channelID.send(view=view)
    for channel in guild.channels:
        if channel.name == channel_com_name:
            print("bot-log channel already exists")
            return
    channel_command = await guild.create_text_channel(channel_com_name)
    await channel_command.set_permissions(role,read_messages=True,send_messages=False)
    await channel_command.set_permissions(everyone,read_messages=False,send_messages=False)
    command_channel_ids = channel_command.id
@bot.event
async def on_member_join(member):#done
    guild = member.guild
    member_role = discord.utils.get(guild.roles, name="member")
    if member_role is not None:
        await member.add_roles(member_role)
@bot.listen()
@commands.has_permissions(moderate_members=True)
async def on_message(message):#semi-done
    words = ["nigga","fuck"]
    if message.author.bot:
        return 
    user = message.author
    role = discord.utils.get(message.guild.roles, name="mute")
    for word in words:
        if word in message.content:
            await user.add_roles(role,reason="saying bad word")
            await message.delete()
            channel = bot.get_channel(command_channel_id)
            await channel.send(f"{user.mention} has been muted for saying {word}")
            return
print(command_channel_id)
@bot.command(name="cltk")
async def cltk(ctx):
    channel = Menu().channel_id
    is_channel = bot.get_channel(channel)
    if is_channel:
        await is_channel.delete()
    else:
        await ctx.send(f"{channel} does not existe")
@bot.command(name="mute")
@commands.has_permissions(mute_members=True)
async def mute(ctx, member:discord.Member,duration:int,*,reason:None):#done
    duration_sec = conver_duration(duration)
    is_admin = discord.utils.get(ctx.guild.roles, name="admin")
    if ctx.author.roles is not is_admin:
        await ctx.send(f"{ctx.author.mention} you are not admin")
        return
    if ctx.author == member:
        await ctx.send(f"{ctx.author.mention} you cant mute your self")
        return
    is_muted = discord.utils.get(ctx.guild.roles, name="mute")
    if member.roles is is_muted:
        await ctx.send(f"{ctx.author.mention} {member.mention} is already muted")
        return
    await member.add_roles(is_muted)
    await command_channel_id.send(f"{member.mention} has been muted for {duration}.")
    await ctx.send(f"{member.mention} has been muted for {duration}.")
    await asyncio.sleep(duration_sec)
    await member.remove_roles(is_muted)
    await command_channel_id.send(f"{member.mention} has been unmuted.")
@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, mem:discord.Member,*, reason=None):#done
    role = discord.utils.get(ctx.author.roles, name="admin")
    if role is not None and role.name == "admin":  
        if mem == None or mem == ctx.message.author:
            await ctx.send("You can't ban yourself!")
            return
        if reason == None:
            reason = "No reason provided"
        message = f"You have been kicked from {ctx.guild.name} for {reason}"
        channel = bot.get_channel(command_channel_id)
        await channel.send(f"{mem.mention} has been kicked for {reason}")
        await mem.send(message)
        await ctx.guild.kick(mem, reason=reason)
    else:
        await ctx.send(f"{ctx.author.mention} you dont have admin")
        return
@bot.command(name="banID")
@commands.has_permissions(ban_members=True)
async def banID(ctx, id: int,*, reason=None):#done
    user = await bot.fetch_user(id)
    role = discord.utils.get(ctx.author.roles, name="admin")
    if role is not None and role.name == "admin":
        if user == ctx.message.author:
            await ctx.send(f"{ctx.author.mention} you are cant ban yourself")
        channel = bot.get_channel(1241131391501074615)
        await channel.send(f"{user.mention} has been banned for {reason}")
        await ctx.guild.ban(user)
    else:
        await ctx.send(f"{ctx.author.mention} you dont have admin")
        return
@bot.command(name="ping")
async def ping(ctx):#done???
    await ctx.send("Pong!")
@bot.command(name="mention")
async def mention(ctx):#done
    await ctx.send("@everyone")
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, mem:discord.Member,*, reason=None):#done
    role = discord.utils.get(ctx.author.roles, name="admin")
    if role is not None and role.name == "admin":  
        if mem == None or mem == ctx.message.author:
            await ctx.send("You can't ban yourself!")
            return
        if reason == None:
            reason = "No reason provided"
        message = f"You have been banned from {ctx.guild.name} for {reason}"
        channel = bot.get_channel(command_channel_id)
        await ctx.send(f"{mem.mention} has been banned for {reason}")
        await mem.send(message)
        await ctx.guild.ban(mem, reason=reason)
        await channel.send(f"{mem} has been banned for {reason}")
    else:
        await ctx.send(f"{ctx.author.mention} you dont have admin")
        return
@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):#done
    user = await bot.fetch_user(id)
    role = discord.utils.get(ctx.author.roles, name="admin")
    if role is not None and role.name == "admin":
        if user == ctx.message.author:
            await ctx.send(f"{ctx.author.mention} you are not banned")
        channel = bot.get_channel(command_channel_id)
        await ctx.guild.unban(user)
        await channel.send(f"{user} has been unbanned")
    else:
        await ctx.send(f"{ctx.author.mention} you dont have admin")
        return
bot.run(token)