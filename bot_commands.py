from cfg import settings  # see note in README.md
prefix = settings['discordAPI']['prefix']

bot_cmds = {
    'help': {
        'brief': 'show commands help',
        'description': 'Show commands help',
        'usage':  f'Usages:\n{prefix}help - list all available commands\n'
                  f'{prefix}help [command] - show help on selected command',
    },
    'about': {
        'brief': 'about this bot',
        'description': 'Show info about this bot',
        'usage': f'Usage:\n{prefix}about'
    },
    'cv': {
        'brief': 'convert reddit media into embedded file',
        'description': 'Convert Reddit URL into embedded image/link. '
                       'Works with: GIF posts, single-image posts, '
                       'post that use external links (Imgur, '
                       'YouTube, Wikipedia etc)',
        'usage': f'Usage:\n{prefix}cv [Reddit_URL]'
    },
    'cvt': {
        'brief': 'extract text from reddit post',
        'description': 'Extracts text from reddit post (command primarily '
                       'meant for r/copypasta)',
        'usage': f'Usage: \n{prefix}cvt [Reddit_URL]'
    }
}

cmd_keys_list = list()
for c in bot_cmds:
    cmd_keys_list.append(c)  # returns map keys
