# RedditToDiscordShare (RTDS)

Bot made explicitly to extract 
images/links & text from Reddit links
and post them as embedded files 
-- so your friends/server-mates don't have to open post
in reddit app (ultimate time saver!)

**Tested and works with**:
- Normal & "share" links
- Links with brackets '<', '>'
- Posts that contain external links (such as YouTube, Imgur, Wikipedia)
- GIF posts
- NSFW posts

**Doesn't work with**:
- Reddit videos
- Gallery (multi-picture) posts

**Invite bot to your server**:
* [click me](https://discord.com/api/oauth2/authorize?client_id=975771580993003540&permissions=274878024768&scope=bot) [0% uptime, looking for new hosts]

---
### Usage
```
,help - list all commands
,cv [Submission_URL] - extract image/link from selected post  
,cvt [Submission_URL] - extract text from selected post  
```
Example:  
![image](image.png)

---
### Dependencies
```
Python ~= 3.8.10
py-cord >= 1.7.3
asyncpraw >= 7.5.0
```
Work on older Python versions not guaranteed

---
### 'cfg.py' contents
```
settings = {
    'discordAPI': {
        'token': 'bot_private_token',
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
