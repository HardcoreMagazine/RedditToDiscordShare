# RedditToDiscordShare (RTDS)
*This is an experimental branch, only used for testing*  
*[>>Stable branch<<](https://github.com/HardcoreMagazine/RedditToDiscordShare/tree/master)*

### Usage
```
/exi [Submission_URL] - extract image/link from selected post  
/ext [Submission_URL] - extract text from selected post  
```

---
### Dependencies
```
Python == 3.8.10
py-cord == 2.3.2
asyncpraw == 7.6.1
```
Note that work with previous or future versions is not guaranteed!

---
### 'cfg.py' contents
```
settings = {
    'discordAPI': {
        'token': 'bot_private_token'
    },
    'redditAPI': {
        'client_id': 'client_id',
        'client_secret': 'secret',
        'password': 'password',  # optional for public submissions
        'user_agent': 'Reddit -> Discord link extraction (by u/HardcoreMagazine)',
        'username': 'username',  # optional for public submissions
    }
}
```
