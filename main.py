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
    # remove brackets if used
    result = 'error'
    try:
        reddit_agent = asyncpraw.Reddit(
            client_id=cfg.settings['redditAPI']['client_id'],
            client_secret=cfg.settings['redditAPI']['client_secret'],
            user_agent=cfg.settings['redditAPI']['user_agent']
        )  # creates read-only instance
        submission = await reddit_agent.submission(url=converted_message)
        result = submission.url
        await reddit_agent.close()  # closes instance
        await context.channel.send(result)
    except Exception as exc:
        print(f'@ Exception has occurred: {exc}')
        await context.channel.send('Reddit API is currently down, please try again later.')

bot.run(cfg.settings['discordAPI']['token'])  # creates discord bot instance
# code below this line execute on script shutdown
print('@ Shutdown in progress')

