import asyncpraw
from discord.ext import commands as cmd
import cfg  # see note in README.md

bot = cmd.Bot(command_prefix=cfg.settings['discordAPI']['prefix'])
reddit_agent = asyncpraw.Reddit(
    client_id=cfg.settings['redditAPI']['client_id'],
    client_secret=cfg.settings['redditAPI']['client_secret'],
    user_agent=cfg.settings['redditAPI']['user_agent']
)  # creates single (shared) read-only reddit instance


@bot.event
async def on_ready():
    print(f'@ Boot successful. Logged as {bot.user}')
    # tells host if bot is ready to use
    print(f'@ Permissions: read-only={reddit_agent.read_only}')
    # tells if bot has permissions to read/write comments && posts
    # note: first command executed after boot runs a lot slower than usual
    # (reddit/discord API "feature")


@bot.command(brief='About this bot', description='About this bot')
async def about(context):
    await context.channel.send(f'Open source Discord bot that converts '
                               f'reddit \'share\' links into embedded files. '
                               f'Project page on Github: '
                               f'<https://github.com/HardcoreMagazine/RedditToDiscordShare>')


@bot.command(brief='Convert reddit link', description='Convert reddit link into embedded image or video')
async def cv(context, message):
    # ***should probably use RegEx for this one***
    if 'reddit' not in message:
        # checks if message contains 'reddit' keyword
        if 'http' in message:
            # shade message if contains link to another website
            await context.channel.send(f'\'<{message}>\' is not a Reddit link')
        else:
            await context.channel.send(f'\'{message}\' is not a Reddit link')
    else:
        typesafe_message = message.replace("<", "").replace(">", "")
        # remove brackets from link (if present; else pass)
        try:
            submission = await reddit_agent.submission(url=typesafe_message)
            # request all data from selected post
            embedded_link = submission.url
            await context.channel.send(embedded_link)
        except Exception as exc:
            await context.channel.send('Invalid link / Reddit API is down, try again later.')
            print(f'@ An exception has occurred: {exc}')


@cv.error  # MissingRequiredArgument error handler for 'cv' command
async def on_command_error(context, error):
    if isinstance(error, cmd.MissingRequiredArgument):
        await context.channel.send('Missing line argument.\n'
                                   'Command usage: `,cv submission_URL`')
        print(f'@ An exception has occurred: {error}')


bot.run(cfg.settings['discordAPI']['token'])  # creates discord bot instance
# code below this line executes on script shutdown
print('@ Shutdown in progress')
reddit_agent.close()  # unsafe: method is not awaited


'''
async def my():
    await reddit_agent.close()
    # closes reddit instance on shutdown
    # unsafe: may not work as intended or work at all
'''
# neither of these two works
