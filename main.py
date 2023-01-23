import asyncio
import re
import asyncpraw
from asyncpraw import exceptions as rexc
from discord.ext import commands as cmd
from cfg import settings  # see note in README.md


bot = cmd.Bot(help_command=None)  # create discord instance
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
    print(f'@ Boot successful. Logged as {bot.user}, slash command mode')
    # tells host if bot is ready to use
    print(f'@ Permissions: Reddit.read_only={reddit_agent.read_only}')
    # tells if bot has permissions to read/write comments && posts


@bot.slash_command(name='about', description='General bot information')
async def _about(context):
    await context.respond(f'Open source Discord bot used for extracting '
                          f'content from reddit posts.\n'
                          f'Project page on Github: '
                          f'<https://github.com/HardcoreMagazine/RedditToDiscordShare>')


'''
@Note:
ping command is excluded from 'stable' branch due to exception that keeps
rising regardless of try-catch block and on_slash_command_error handler
'''
@bot.slash_command(name='ping', description='Shows bot latency in milliseconds')
@cmd.cooldown(1, 60, cmd.BucketType.guild)
async def ping(context):
    await context.respond(f"Latency: `{int(bot.latency * 1000)} ms`.")


@bot.slash_command(name='exi', description='Extract image/links from selected post')
async def _exi(context, url):
    typesafe_url = url.replace("<", "").replace(">", "").replace("|", "")
    try:
        await context.defer() # wait for reddit API response
        submission = await reddit_agent.submission(url=typesafe_url)
        # request all data from selected post
        embedded_link = submission.url
        await context.respond(embedded_link)
    except Exception as exc:
        if isinstance(exc, rexc.InvalidURL):
            await context.respond('Invalid reddit URL')
        elif isinstance(exc, rexc.RedditAPIException):
            await context.respond('Reddit API error, try again later')
        else:
            print(f'@ An exception has occurred: "{exc}"')


@bot.slash_command(name='ext', description='Extract text from selected post')
async def _ext(context, url):
    typesafe_url = url.replace("<", "").replace(">", "").replace("|", "")
    try:
        await context.defer() # wait for reddit API response
        submission = await reddit_agent.submission(url=typesafe_url)
        # request all data from selected post
        s_title = submission.title
        s_text: str = submission.selftext
        max_text_size = 2000
        if len(s_text) > max_text_size:
            await context.respond(f'Submission contains more than {max_text_size} '
                                  f'characters, unable to process '
                                  f'due to Discord limitations')
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
            # hide all included links ("HTTP(S)://") in <> brackets
            s_text = s_text.replace("&#x200B;", '')
            # "&#x200B;" - zero-width space character
            # pops up occasionally due to random
            # errors on reddit side
            await context.respond(f'> {s_title}\n\n'
                                  f''  # escape discord quote
                                  f'{s_text}')
    except Exception as exc:
        if isinstance(exc, rexc.InvalidURL):
            await context.respond('Invalid URL')
        elif isinstance(exc, rexc.RedditAPIException):
            await context.respond('Reddit API is down, try again later')
        print(f'@ An exception has occurred: "{exc}"')


@bot.event  # universal error handler for commands
async def on_slash_command_error(context, error):
    if isinstance(error, cmd.CommandOnCooldown): # doesnt work
        await context.respond('Command on cooldown')
    else:
        print(f'@ An exception has occurred: "{error}"')


bot.run(settings['discordAPI']['token'])  # creates discord bot instance
# code below this line executes on program shutdown
print('@ Shutdown in progress')
asyncio.run(shutdown())
