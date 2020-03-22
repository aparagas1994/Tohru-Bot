import discord
import asyncio
import traceback
import signal
from discord.ext import commands
from logutils import logger
from sigterm_handler import sigterm_handler
from tohruToken import TOKEN

bot = commands.Bot(command_prefix='/', description="Tohru Bot")

@bot.event
async def on_ready():
    signal.signal(signal.SIGTERM, sigterm_handler)
    print("bot ready")
    # await bot.change_presence(game=discord.Game(name='with Kanna'))

@bot.event
async def on_message(message):
    logger.debug("Received message [%s:%s:%s:%s]: %s" % (message.channel, message.channel.id, message.author.name, message.author.id, message.content))
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.channel, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.channel, 'Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        await bot.send_message(ctx.message.channel, "Oh so sorry, I've messed up the order, would you like some dragon tail instead? teehee")
        logger.error('In {0.command.qualified_name}:'.format(ctx))
        for line in traceback.format_tb(error.original.__traceback__):
            logger.error(line)
        logger.error('{0.__class__.__name__}: {0}'.format(error.original))

if __name__ == "__main__":
    from commands import *
    bot.run(TOKEN)

