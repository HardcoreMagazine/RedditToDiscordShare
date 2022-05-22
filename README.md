# RedditToDiscordShare (RTDS) 
*This is a stable version*  
*[Experimental branch](https://github.com/HardcoreMagazine/RedditToDiscordShare/tree/experimental)*

Bot made explicitly to extract 
image/video links from reddit 'share' links
and post them as embedded files 
-- so your friends/server-mates don't have to open post
in reddit app (ultimate time saver!)

**Tested and works with**:
- Normal & "share" links
- Links with brackets "<", ">"
- External links (YouTube, Imgur, Wikipedia and others)
- GIF posts
- NSFW posts  

**Doesn't work with**:
- Reddit videos
- Gallery (multi-picture) posts

---
### Usage
```
,cl [URL] - extract element-link from reddit post  
```
Example:  
![](image.png)

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
