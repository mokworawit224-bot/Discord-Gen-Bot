import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_IDS = {503783432397127680}  

locked_mute = set()
locked_deafen = set()

def is_owner(user_id):
    return user_id in OWNER_IDS

# 🎛️ UI ปุ่ม
class ControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # 🔇 Lock Mute
    @discord.ui.button(label="Lock Mute", style=discord.ButtonStyle.danger)
    async def lock_mute(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_owner(interaction.user.id):
            return await interaction.response.send_message("❌ ไม่มีสิทธิ์", ephemeral=True)

        if not interaction.user.voice:
            return await interaction.response.send_message("❌ คุณต้องอยู่ในห้องเสียง", ephemeral=True)

        channel = interaction.user.voice.channel

        for member in channel.members:
            if member.id not in OWNER_IDS:
                await member.edit(mute=True)
                locked_mute.add(member.id)

        await interaction.response.send_message("🔒 ล็อกไมค์แล้ว", ephemeral=True)

    # 🔊 Unlock Mute
    @discord.ui.button(label="Unlock Mute", style=discord.ButtonStyle.success)
    async def unlock_mute(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_owner(interaction.user.id):
            return await interaction.response.send_message("❌ ไม่มีสิทธิ์", ephemeral=True)

        channel = interaction.user.voice.channel

        for member in channel.members:
            await member.edit(mute=False)
            locked_mute.discard(member.id)

        await interaction.response.send_message("🔓 ปลดไมค์แล้ว", ephemeral=True)

    # 🔕 Lock Deafen
    @discord.ui.button(label="Lock Deafen", style=discord.ButtonStyle.danger)
    async def lock_deafen(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_owner(interaction.user.id):
            return await interaction.response.send_message("❌ ไม่มีสิทธิ์", ephemeral=True)

        channel = interaction.user.voice.channel

        for member in channel.members:
            if member.id not in OWNER_IDS:
                await member.edit(deafen=True)
                locked_deafen.add(member.id)

        await interaction.response.send_message("🔒 ล็อกหูแล้ว", ephemeral=True)

    # 🔔 Unlock Deafen
    @discord.ui.button(label="Unlock Deafen", style=discord.ButtonStyle.success)
    async def unlock_deafen(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_owner(interaction.user.id):
            return await interaction.response.send_message("❌ ไม่มีสิทธิ์", ephemeral=True)

        channel = interaction.user.voice.channel

        for member in channel.members:
            await member.edit(deafen=False)
            locked_deafen.discard(member.id)

        await interaction.response.send_message("🔓 ปลดหูแล้ว", ephemeral=True)

# 🛡 กัน override (กันทุกคน)
@bot.event
async def on_voice_state_update(member, before, after):

    if member.id in locked_mute and not after.mute:
        await member.edit(mute=True)

    if member.id in locked_deafen and not after.deaf:
        await member.edit(deafen=True)

# 🎛️ คำสั่งเปิด Panel
@bot.command()
async def panel(ctx):
    embed = discord.Embed(
        title="⚠️ GEN CORE CONTROL ⚠️",
        description="```diff\n- ห้ามปลดเอง / ระบบล็อกขั้นสูง\n+ Owner เท่านั้นที่ควบคุมได้\n```",
        color=discord.Color.red()
    )

    embed.add_field(name="🔇 Lock Mute", value="ปิดไมค์ทั้งหมด", inline=False)
    embed.add_field(name="🔊 Unlock Mute", value="ปลดไมค์", inline=False)
    embed.add_field(name="🔕 Lock Deafen", value="ปิดหูทั้งหมด", inline=False)
    embed.add_field(name="🔔 Unlock Deafen", value="ปลดหู", inline=False)

    embed.set_footer(text="GEN CORE SYSTEM")

    await ctx.send(embed=embed, view=ControlView())

bot.run("MTQ4OTYwOTczNTcxNDg5ODA4Mg.G5Pi_F.oCtAXy5XldiEx8kep9QeBa_xr8bXMpOTXCnpa8")