import asyncio
import re
import asyncpraw
from asyncpraw import exceptions as rexc
from discord.ext import commands as cmd
from bot_commands import bot_cmds
from bot_commands import cmd_keys_list
from cfg import settings  # see note in README.md

prefix = settings['discordAPI']['prefix']
bot = cmd.Bot(
    command_prefix=prefix,
    help_command=None
)  # create discord instance
reddit_agent = asyncpraw.Reddit(
    client_id=settings['redditAPI']['client_id'],
    client_secret=settings['redditAPI']['client_secret'],
    user_agent=settings['redditAPI']['user_agent']
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


@bot.command()
async def about(context):
    await context.channel.send(f'Open source Discord bot that converts '
                               f'reddit "share" links into embedded files/text.\n'
                               f'List all available commands: `{prefix}help`\n'
                               f'Project page on Github: '
                               f'<https://github.com/HardcoreMagazine/RedditToDiscordShare>')


@bot.command()
async def cv(context, message):
    typesafe_url = message \
        .replace("<", "").replace(">", "") \
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


@bot.command()
async def cvt(context, message):
    typesafe_url = message \
        .replace("<", "").replace(">", "") \
        .replace("|", "")
    # remove garbage from URL if present
    try:
        submission = await reddit_agent.submission(url=typesafe_url)
        # request all data from selected post
        s_title = submission.title
        s_text: str = submission.selftext
        if len(s_text) > 4000:
            await context.channel.send('Submission contains more than 4000 '
                                       'characters, unable to process '
                                       'due to Discord limitations')
        else:
            regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)" \
                    r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))" \
                    r"+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)" \
                    r"|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            link_list = re.findall(regex, s_text)
            if link_list:  # if list is not empty
                for link in link_list:
                    conv_link = ''.join(link)
                    s_text = s_text.replace(conv_link, f"<{conv_link}>")
            # hide all internal links ("HTTP(S)://") in <> brackets
            s_text = s_text.replace("&#x200B;", '')
            # "&#x200B;" - zero-width space character
            # pops up occasionally due to random
            # errors on Reddit side
            await context.channel.send(f'> **{s_title}**\n\n'
                                       f''  # escape discord quote
                                       f'{s_text}')
    except Exception as exc:
        if isinstance(exc, rexc.InvalidURL):
            await context.channel.send('Invalid URL')
        elif isinstance(exc, rexc.RedditAPIException):
            await context.channel.send('Reddit API is down, try again later')
        print(f'@ An exception has occurred: "{exc}"')


@bot.command()
async def help(context, message=None):
    if message is None:
        msg = '```Available commands:\n\n'
        for c in cmd_keys_list:
            msg += f'{c} - {bot_cmds[c]["brief"]}\n'
        msg += f'\nUse {prefix}help [command] ' \
               f'to show help on specific command```'
        await context.send(msg)
    else:
        if message in cmd_keys_list:
            await context.channel.send(f'```{bot_cmds[message]["description"]}\n\n'
                                       f'{bot_cmds[message]["usage"]}```')
        else:
            await context.channel.send(f'Command "{message}" not found\n'
                                       f'Use `{prefix}help` to '
                                       f'list all available commands')


@bot.event  # universal error handler for commands
async def on_command_error(context, error):
    if isinstance(error, cmd.CommandNotFound):
        await context.channel.send(f'Unrecognized command\n'
                                   f'Use `{prefix}help` to list '
                                   f'all available commands')
    elif isinstance(error, cmd.MissingRequiredArgument):
        await context.channel.send(f'Missing line argument\n'
                                   f'Use: `{prefix}help [command]`')
    print(f'@ An exception has occurred: "{error}"')


bot.run(settings['discordAPI']['token'])  # creates discord bot instance
# code below this line executes on script shutdown
print('@ Shutdown in progress')
asyncio.run(shutdown())
