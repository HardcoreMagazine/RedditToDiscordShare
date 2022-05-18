import asyncpraw
from discord.ext import commands as cmd
import cfg  # see note in README.md

bot = cmd.Bot(command_prefix=cfg.settings['discordAPI']['prefix'])


@bot.event
async def on_ready():
    print(f'@ Boot successful. Logged as {bot.user}')  # tells host if bot is ready to use


@bot.command(brief='About this bot', description='About this bot')
async def about(context):
    await context.channel.send(f'Open source Discord bot that converts '
                               f'reddit \'share\' links into embedded files. '
                               f'Project page on Github: '
                               f'<https://github.com/HardcoreMagazine/RedditToDiscordShare>')


@bot.command(brief='Convert reddit link', description='Convert reddit link into embedded image or video')
async def cv(context, message):
    converted_message = message.replace("<", "").replace(">", "")
    # remove brackets from link (if present)
    reddit_agent = asyncpraw.Reddit(
        client_id=cfg.settings['redditAPI']['client_id'],
        client_secret=cfg.settings['redditAPI']['client_secret'],
        user_agent=cfg.settings['redditAPI']['user_agent']
    )  # creates read-only reddit instance
    # slow && safe method to talk with API
    try:
        submission = await reddit_agent.submission(url=converted_message)
        result = submission.url
        await context.channel.send(result)
    except Exception as api_exc:
        await context.channel.send('Invalid URL / Reddit API is down, try again later.')
        await reddit_agent.close()  # closes reddit instance
        print(f'@ An exception has occurred: {api_exc}')
    await reddit_agent.close()  # closes reddit instance


@cv.error  # MissingRequiredArgument error handler for 'cv' command
async def on_command_error(context, error):
    if isinstance(error, cmd.MissingRequiredArgument):
        await context.channel.send('Missing line argument.\n'
                                   'Use: `,cv submission_URL`')
        print(f'@ An exception has occurred: {error}')


bot.run(cfg.settings['discordAPI']['token'])  # creates discord bot instance
# code below this line executes on script shutdown
print('@ Bot shutdown in progress')
