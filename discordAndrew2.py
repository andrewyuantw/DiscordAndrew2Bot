import discord
from discord.ext import commands

import os
import time
import random

bot = commands.Bot(command_prefix='!')

# These are global variables that I've declared for my bot that would differ for each user. 
# I've put garbage values for each variable 

PATH_TO_FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe"
PATH_TO_AUDIO = "C:/DiscordBot"
BOT_TOKEN = "XXXXXXXX"
MY_USER_ID = 1234567890
ANDREW_2_ID = 1234567890
TEXT_CHANNEL_ID = 1234567890
VOICE_CHANNEL_ID = 1234567890

# Since our server has two other bots (Rhythm and Groovy) I've added their IDs so when we get 
# a random person in a voice channel, a bot won't get chosen
GROOVY_BOT_ID = 1234567890
RHYTHM_BOT_ID = 1234567890
      
# Prints message to console when ready      
@bot.event
async def on_ready():
    print("I am here")

# Bot joins the voice channel in which the caller is currently in 
@bot.command()
async def join(ctx):
    voiceChannel = ctx.author.voice
    if voiceChannel != None:
        await voiceChannel.channel.connect() 
    else:
        await ctx.send(str(ctx.author.name) + " is not in a channel")

# Bot leaves the voice channel
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

# Gives a list of commands that may be used 
@bot.command()
async def commands(ctx):
    await ctx.send(
        "You can use the following commands:\n !skr\n !hi\n !haiyaa\n" 
        " !fuiyoh\n !no\n !really \n !randommessage\n !voice \n"
    )

# Bot responds when either I am mentioned, or the bot is mentioned
@bot.event
async def on_message(message):
    mention = f'<@!{MY_USER_ID}>'
    if mention in message.content:
        await message.channel.send("誰@了帥哥")
    
    mention = f'<@!{ANDREW_2_ID}>'
    if mention in message.content:
        await message.channel.send("LMAO leave me alone")

    await bot.process_commands(message)

# Function to play a clip in the voice channel of the caller 
async def playAudio(ctx, audioFile):
    voice = ctx.voice_client
    if voice == None:
        # If not connected, then we connect to the voice channel of the caller
        print("not connected")
        voice = await ctx.author.voice.channel.connect()
    else:
        # If we are already connected, then no action is required
        print("already connected")

    voice.play(discord.FFmpegPCMAudio(executable= PATH_TO_FFMPEG, source= PATH_TO_AUDIO + audioFile))
    # Sleep while audio is playing
    while voice.is_playing():
        time.sleep(.1)

# Plays meme/anime/in-joke clips in the voice channel
@bot.command()
async def hi(ctx):
    await playAudio(ctx, "/hi.mp3")

@bot.command()
async def skr(ctx):
    await playAudio(ctx, "/skr.mp3")

@bot.command()
async def no(ctx):
    await playAudio(ctx, "/no.mp3")

@bot.command()
async def really(ctx):
    await playAudio(ctx, "/really.mp3")

# Plays Uncle Roger's two catchphrases
@bot.command()
async def haiyaa(ctx):
    await playAudio(ctx, "/haiyaa.mp3")

@bot.command()
async def fuiyoh(ctx):
    await playAudio(ctx, "/fuiyoh.mp3")

# Gets a random message from a selected text channel
@bot.command()
async def randommessage(ctx):
    
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    if channel == None:
        await ctx.send("No such channel.")
        return

    # Gets the last 300 messages and stores in an array
    messages = []
    async for message in channel.history(limit=300):
        messages.append(message)

    # Chooses a random message
    randomMessage = random.choice(messages).content

    await ctx.send(
        f'Random message in {channel.name}:\n' + randomMessage
    )

# Selects a random member from a selected voice channel
@bot.command()
async def voice(ctx):

    VC = discord.utils.get(ctx.guild.channels, id=VOICE_CHANNEL_ID)
    
    # Goes through the members, and stores non robot members in a separate array
    toPost = "People in this channel: \n"
    nonRobot = []
    for user in VC.members:
        toPost += str(user.name) + " "
        if user.id != ANDREW_2_ID and user.id != GROOVY_BOT_ID and user.id != RHYTHM_BOT_ID:
            nonRobot.append(user)
    
    if (len(nonRobot) == 0):
        await ctx.send("No one is in the channel right now")
        return

    # Selects random member from the nonRobot array
    user = random.choice(nonRobot)

    await ctx.send(toPost + "\n")
    await ctx.send(f'That\'s {len(nonRobot)} person/people and {len(VC.members)} people/robots total')
    await ctx.send(f'{user.mention} is the chosen one')

bot.run(BOT_TOKEN)
