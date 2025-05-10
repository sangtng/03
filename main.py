import discord
from discord import app_commands
from discord.ext import commands
import json
import os

TOKEN = "MTM3MDI1Mzg4NDQxNjg1MjA0OA.G1Sb0B.r7g4z_AthkJlPtZfVuWyTpDMiWP1UWJ9f2hk3E"
GUILD_ID = discord.Object(id=1367682108071481437)  # แก้เป็นเลข guild ของคุณ

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "profiles.json"

if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
    with open(DATA_FILE, "r") as f:
        profiles = json.load(f)
else:
    profiles = {}

@bot.event
async def on_ready():
    await bot.tree.sync(guild=GUILD_ID)
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.tree.command(name="set_profile", description="Set a profile for yourself or another member", guild=GUILD_ID)
@app_commands.describe(
    user="The member to set profile for (optional)",
    rank="Your ROV rank",
    winrate="Your winrate percentage",
    kda="Your KDA",
    nickname="Your nickname",
    ingame_name="Your in-game name",
    avatar="Avatar URL"
)
async def set_profile(interaction: discord.Interaction,
                      user: discord.Member = None,
                      rank: str = "",
                      winrate: float = 0.0,
                      kda: float = 0.0,
                      nickname: str = "",
                      ingame_name: str = "",
                      avatar: str = ""):
    target = user or interaction.user
    profiles[str(target.id)] = {
        "rank": rank,
        "winrate": winrate,
        "kda": kda,
        "nickname": nickname,
        "ingame_name": ingame_name,
        "avatar": avatar
    }
    with open(DATA_FILE, "w") as f:
        json.dump(profiles, f, indent=4)

    await interaction.response.send_message(f"Profile for {target.mention} has been updated!", ephemeral=True)

@bot.tree.command(name="profile", description="Show profile", guild=GUILD_ID)
@app_commands.describe(user="User to view profile of (optional)")
async def profile(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    data = profiles.get(str(target.id))

    if not data:
        await interaction.response.send_message("Profile not found.", ephemeral=True)
        return

    embed = discord.Embed(title=f"{data.get('nickname', target.name)}'s Profile",
                          color=discord.Color.red())
    embed.set_thumbnail(url=data.get("avatar") or target.avatar.url if target.avatar else discord.Embed.Empty)
    embed.add_field(name="Rank", value=data.get("rank", "N/A"), inline=True)
    embed.add_field(name="Winrate", value=f"{data.get('winrate', 0)}%", inline=True)
    embed.add_field(name="KDA", value=str(data.get("kda", "N/A")), inline=True)
    embed.add_field(name="In-game Name", value=data.get("ingame_name", "N/A"), inline=True)
    embed.set_footer(text="Guild: สังข์")

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)