# 0xdeadbeef-Markov-Discord

A discord bot which use webhook and markov chain to imitate channel members.  
If used for scale it needs to be modify, it was built to be used on only 1 server.  

Install & Run:

```
$ pip3 install -r requirements.txt
$ echo -n 'discord_token=<discord_bot_token>' > .env
```

- Invite the bot to a discord server

- Run `fetchmsg.py`
- Go on discord and type `fetch` in a channel where the bot is present (adjust your name at the top of the on_message functions in `fetchmsg.py`). (it may take a while to finish)
- ^^ this step is only used if you need an initial dataset, you can let the bot run and the dataset will build on it's own
- Run `main.py`
