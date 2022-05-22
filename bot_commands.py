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
        'brief': 'convert reddit links',
        'description': 'Convert Reddit URL into embedded image/link',
        'usage': f'Usage:\n{prefix}cv [Reddit_URL]'
    }
    # to be continued...
}

cmd_keys_list = list()
for c in bot_cmds:
    cmd_keys_list.append(c)  # returns keys
