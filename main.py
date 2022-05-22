import asyncio
import asyncpraw
from asyncpraw import exceptions as rexc
from discord.ext import commands as cmd
import cfg  # see note in README.md

prefix = cfg.settings['discordAPI']['prefix']
bot = cmd.Bot(command_prefix=prefix)
# create discord instance
reddit_agent = asyncpraw.Reddit(
    client_id=cfg.settings['redditAPI']['client_id'],
    client_secret=cfg.settings['redditAPI']['client_secret'],
    user_agent=cfg.settings['redditAPI']['user_agent']
)  # creates single (shared) read-only reddit instance


async def shutdown():
    # safe log-out from reddit && discord
    await reddit_agent.close()
    await bot.close()


@bot.event
async def on_ready():
    print(f'@ Boot successful. Logged as {bot.user}, prefix: "{prefix}"')
    # tells host if bot is ready to use
    print(f'@ Permissions: read_only={reddit_agent.read_only}')
    # tells if bot has permissions to read/write comments && posts


@bot.command(brief='About this bot', description='About this bot')
async def about(context):
    await context.channel.send(f'Open source Discord bot that converts '
                               f'reddit \'share\' links into embedded files. '
                               f'List all available commands: `{prefix}help`\n'
                               f'Project page on Github: '
                               f'<https://github.com/HardcoreMagazine/RedditToDiscordShare>')


@bot.command(brief='Convert reddit link', description='Convert reddit URL into embedded image or video')
async def cv(context, message):
    typesafe_url = message\
        .replace("<", "").replace(">", "")\
        .replace("|", "")
    # remove garbage from URL if present
    try:
        submission = await reddit_agent.submission(url=typesafe_url)
        # request all data from selected post
        embedded_link = submission.url
        await context.channel.send(embedded_link)
    except Exception as exc:
        if isinstance(exc, rexc.InvalidURL):
            await context.channel.send('Invalid URL')
        elif isinstance(exc, rexc.RedditAPIException):
            await context.channel.send('Reddit API is down, try again later')
        print(f'@ An exception has occurred: "{exc}"')


@bot.event  # universal error handler for commands
async def on_command_error(context, error):
    if isinstance(error, cmd.CommandNotFound):
        await context.channel.send(f'Unrecognized command\n'
                                   f'Use `{prefix}help` to list '
                                   f'all available commands')
    if isinstance(error, cmd.MissingRequiredArgument):
        await context.channel.send(f'Missing line argument\n'
                                   f'Use: `{prefix}help [command]`')
    print(f'@ An exception has occurred: "{error}"')


bot.run(cfg.settings['discordAPI']['token'])  # creates discord bot instance
# code below this line executes on script shutdown
print('@ Shutdown in progress')
asyncio.run(shutdown())
