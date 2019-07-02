import os
import discord
from discord.ext import commands
from discord.ext.commands import Context

with open("token.txt", 'r') as f:
    TOKEN = f.read().strip()

bot = commands.Bot(command_prefix=".")


def create_command(name):
    @commands.command(name=name[:-4])
    async def command(ctx: Context):
        vc = ctx.guild.voice_client
        if vc is None:
            await ctx.author.voice.channel.connect()
            vc = ctx.guild.voice_client
        if vc.is_playing():
            vc.stop()
        audio = discord.FFmpegPCMAudio(f"sounds/{name}", executable="ffmpeg/bin/ffmpeg",
                                       before_options=f'-nostdin -ss {0.0}',
                                       options='-vn -b:a 128k')
        vc.play(audio, after=lambda: print("Success"))
        print(ctx.author)
        await ctx.message.delete()

    return command


@bot.command()
async def leave(ctx: Context):
    return await ctx.voice_client.disconnect()


@bot.command()
async def join(ctx: Context):
    return await ctx.author.voice.channel.connect()


@bot.event
async def on_ready():
    # load_opus()
    print("Logged in as:")
    print(bot.user.name)
    print(bot.user.id)
    print("-------")

for file in os.listdir("sounds"):
    bot.add_command(create_command(file))

bot.run(TOKEN)
