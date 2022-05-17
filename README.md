# RedditToDiscordShare (RTDS)

Bot made explicitly to extract 
image/video links from reddit 'share' links
and post them as embedded files 
-- so your friends/server-mates don't have to open post
in reddit app (ultimate time saver!)

**Tested and works with**:
- Normal links
- Phone "share" links
- Links with brackets "<", ">"
- NSFW posts

**Doesn't work with**:
- Videos (YET!)
- Gallery (multi-picture) posts

---
### Usage
```
,cv [link] - extract image link from reddit post  
```
Example:
![img.png](img.png)

---
### Dependencies:
```
Python >= 3.8.10
py-cord >= 1.7.3
asyncpraw >= 7.5.0
asyncprawcore >= 2.3.0
```
---
### 'cfg.py' contents:
```
settings = {
    'discordAPI': {
        'token': 'bot_private_key',
        'prefix': 'bot_prefix'
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
