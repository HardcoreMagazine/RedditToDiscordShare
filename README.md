# RedditToDiscordShare (RTDS)
*This is an experimental version*  
*[Stable branch](https://github.com/HardcoreMagazine/RedditToDiscordShare/tree/master)*

Bot made explicitly to extract 
image/video links from reddit 'share' links
and post them as embedded files 
-- so your friends/server-mates don't have to open post
in reddit app (ultimate time saver!)

**Tested and works with**:
- Normal & "share" links
- Links with brackets "<", ">"
- External links (such as YouTube, Imgur, Wikipedia)
- GIF posts
- NSFW posts

**Doesn't work with**:
- Reddit videos
- Gallery (multi-picture) posts

**Invite bot to your server**:
* [click me](https://discord.com/api/oauth2/authorize?client_id=975771580993003540&permissions=274878024768&scope=bot)

---
### Usage
```
,cv [Submission_URL] - extract image/link from selected post  
```
Example:  
![image](image.png)

---
### Dependencies:
```
Python >= 3.8.10
py-cord >= 1.7.3
asyncpraw >= 7.5.0
```
---
### 'cfg.py' contents:
```
settings = {
    'discordAPI': {
        'token': 'bot_private_key',
        'prefix': ','
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
