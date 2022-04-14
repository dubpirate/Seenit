# Seenit

_Disclaimer_: This bot uses the Letterboxd API but is not otherwise affiliated
with, endorsed or certified by Letterboxd.

# Getting Started
To get this code working you're going to need some local variables and stuff.

## Aquiring API
You need:
 - Letterboxd API key and Secret (Currently in closed beta, check their 
 website for more details)
 - An account for your reddit bot that uses the format Seenit_(subreddit name)
 - A new Reddit App Details that can be found by clicking the 'create an app' 
 button at the bottom of [this page](https://www.reddit.com/prefs/apps/)

## For Letterboxd
You need to set you Letterboxd API Key and Secret in their respective env 
variables:

 - `LBXD_API_KEY`
 - `LBXD_API_SECRET`

Alternatively, you can create a `secrets.json` file with the following format:

```json
{
	"letterboxd": {
		"key": "----",
		"secret": "----"
	}
}
```

## For Reddit
Then you need to make a `praw.ini` file in the directory you're running the 
script in with the following format:

```ini
...
[Seenit_bot_name]
client_id=[redacted]
client_secret=[redacted]
password=[redacted]
username=Seenit_bot_name
user_agent=[anything you like, really]
```

Most importantly is that the username must match ini block thing at the top.

## How it will work

### Commands:
When a redditor comments `u/Seenit_{subreddit_name} https://lbxd.it/{film_id}`, 
the Seenit Reddit Bot will reply with the average score of all the people it's
following (which will soon be the people from the subreddit). Thereby, it is a
rating by the members of the subreddit.